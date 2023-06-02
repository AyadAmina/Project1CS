from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.template import loader
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       
        self.lieu_id = self.scope['url_route']['kwargs']['lieu_id']
        self.lieu_group_name = 'lieu_%s_comments' % self.lieu_id

        # Join lieu group
        await self.channel_layer.group_add(
            self.lieu_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave lieu group
        await self.channel_layer.group_discard(
            self.lieu_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        comment = text_data_json['comment']
        author = text_data_json['author']

        # Save the comment to the database asynchronously
        await database_sync_to_async(Comment.objects.create)(
            lieu_id=self.lieu_id,
            author=author,
            text=comment
        )
        # Create a notification for the admin
        lieu = await database_sync_to_async(Lieu.objects.get)(pk=self.lieu_id)
        admin_id = await database_sync_to_async(lieu.get_admin_id)()
        admin = await database_sync_to_async(User.objects.get)(idUser=admin_id)
        notification =await database_sync_to_async( Notification.objects.create)(adminreg=admin, lieu=lieu.nomLieu,author=author)

        # Send the comment to the lieu group
        await self.channel_layer.group_send(
            self.lieu_group_name,
            {
                'type': 'comment_message',
                'comment': comment,
                'author': author
            }
        )

    async def comment_message(self, lieu):
        # Send the comment to the WebSocket
        await self.send(text_data=json.dumps({
            'comment': lieu['comment'],
            'author': lieu['author']
        }))


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
def admin(request):
    template = loader.get_template('indexadmin.html')
    return HttpResponse(template.render())
def comm(request):
 
    return render(request,'comm.html')

def lieu(request, lieu_id):
    lieu = Lieu.objects.get(pk=lieu_id)
    username = request.user.username
    return render(request, 'comm.html', {'lieu': lieu,'name':username})

def adminnot(request):
    notifications = Notification.objects.filter(adminreg=request.user.id).order_by('-created_at')[:5]  
    template = loader.get_template('indexadmin.html')
    context = {
        'notifications': notifications
    }
    return HttpResponse(template.render(context, request))




class AdminNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['user'].id
        self.admin_notification_group_name = f'admin_notification_{user_id}'

        # Join admin notification group
        await self.channel_layer.group_add(
            self.admin_notification_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave admin notification group
        await self.channel_layer.group_discard(
            self.admin_notification_group_name,
            self.channel_name
        )

    async def send_notification(self, lieu):
        # Send the notification to the WebSocket
        await self.send(text_data=json.dumps({
            'comment': lieu['comment'],
            'author': lieu['author']
        }))





@login_required  # Restrict access to authenticated users
def update_feedback(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        lieu_id = request.POST.get('lieu_id')
        rating = int(request.POST.get('rating'))
        

        try:
            lieu = get_object_or_404(Lieu, idLieu=lieu_id)

            # Check if the user already has a feedback for the lieu
            existing_feedback = Feedback.objects.filter(user=request.user.id, lieu=lieu).first()

            if existing_feedback:
                # If the user has an existing feedback, update it
                existing_feedback.rating = rating
              
                existing_feedback.save()
            else:
                # Create a new feedback instance
                feedback = Feedback(user=request.user.id, lieu=lieu, rating=rating)
                feedback.save()

            # Update the feedback and number of feedback in the Lieu model
            lieu_feedbacks = Feedback.objects.filter(lieu=lieu)
            num_feedbacks = lieu_feedbacks.count()
            total_rating = sum(feedback.rating for feedback in lieu_feedbacks)
            lieu.feedback = total_rating / num_feedbacks if num_feedbacks > 0 else 0
            lieu.nmb_feedbach = num_feedbacks
            lieu.save()

            return JsonResponse({'success': True})
        except Lieu.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lieu not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def retrieve_feedback(request):
    
    if request.method == 'POST':
        lieu_id = request.POST.get('lieu_id')
        feedback = Feedback.objects.filter(lieu_id=lieu_id)
        num_feedback = feedback.count()
        total_rating = sum(feedback.values_list('rating', flat=True))
        average_rating = round(total_rating / num_feedback) if num_feedback > 0 else 0

        user_rating = 0
        if request.user.is_authenticated:
            user_feedback = feedback.filter(user=request.user.id)
            if user_feedback.exists():
                user_rating = user_feedback.first().rating

        return JsonResponse({
            'feedback': total_rating,
            'num_feedback': num_feedback,
            'average_rating': average_rating,
            'user_rating': user_rating
        })
    else:
        return JsonResponse({'error': 'Invalid request method'})


