from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.template import loader

# Create your views here.

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.event_group_name = 'event_%s' % self.event_id

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
        text_data_json = json.loads(text_data)
        comment = text_data_json['comment']
        author = text_data_json['author']

        # Save the comment to the database
        Comment.objects.create(
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
        comment = event['comment']
        author = event['author']

        # Send comment to WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'author': author
        }))

def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())


def event_detail(request, event_id):
    event = Evenement.objects.get(pk=event_id)
    return render(request, 'comment.html', {'event': event})
