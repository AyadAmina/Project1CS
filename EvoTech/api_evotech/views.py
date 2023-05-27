from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.template import loader
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('haniiiii ')
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.event_group_name = 'event_%s_comments' % self.event_id

        # Join event group
        await self.channel_layer.group_add(
            self.event_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave event group
        await self.channel_layer.group_discard(
            self.event_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print('hello')
        text_data_json = json.loads(text_data)
        comment = text_data_json['comment']
        author = text_data_json['author']

        # Save the comment to the database asynchronously
        await database_sync_to_async(Comment.objects.create)(
            evenement_id=self.event_id,
            author=author,
            text=comment
        )

        # Send the comment to the event group
        await self.channel_layer.group_send(
            self.event_group_name,
            {
                'type': 'comment_message',
                'comment': comment,
                'author': author
            }
        )

    async def comment_message(self, event):
        # Send the comment to the WebSocket
        await self.send(text_data=json.dumps({
            'comment': event['comment'],
            'author': event['author']
        }))


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
def comm(request):
 
    return render(request,'comm.html')

def event_detail(request, event_id):
    event = Evenement.objects.get(pk=event_id)
    username = request.user.username
    return render(request, 'comm.html', {'event': event,'name':username})


    
class AdminNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the admin user's channel name to a group
        admin_username = self.scope['user'].username
        await self.channel_layer.group_add(
            admin_username,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the admin user's channel name from the group
        admin_username = self.scope['user'].username
        await self.channel_layer.group_discard(
            admin_username,
            self.channel_name
        )

    async def admin_notification(self, event):
        notification_id = event['notification_id']

        # Mark the notification as read
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()

        # Send the notification message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': notification.message
        }))