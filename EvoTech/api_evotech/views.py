from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.template import loader
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

from django.http import JsonResponse


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
        lieu = Lieu.objects.get(pk=self.lieu_id)
        admin_id = lieu.get_admin_id()
        admin = User.objects.get(idUser=admin_id)
        notification = Notification.objects.create(adminreg=admin, lieu=lieu.nomLieu,author=author)

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
    notifications = Notification.filter(adminreg=request.user).order_by('-created_at')[:5]  
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



def update_feedback(request):
    print('helooooooooooooooooo')
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        lieu_id = request.POST.get('lieu_id')
        rating = request.POST.get('rating')

        try:
            lieu = Lieu.objects.get(idLieu=lieu_id)
            current_feedback = lieu.feedback
            current_nmb_feedback = lieu.nmb_feedbach

            new_feedback = ((current_feedback * current_nmb_feedback) + float(rating)) / (current_nmb_feedback + 1)
            new_nmb_feedback = current_nmb_feedback + 1

            lieu.feedback = new_feedback
            lieu.nmb_feedbach = new_nmb_feedback
            lieu.save()

            return JsonResponse({'success': True})
        except Lieu.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lieu not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
