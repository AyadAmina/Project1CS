from django.urls import path
from . import views
from .views import CommentConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/event/(?P<event_id>\d+)/comments/$', CommentConsumer.as_asgi()),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('comm/', views.comm, name='comm'),
    
    path('<int:event_id>/', views.event_detail, name='event_detail'),

    
]
