from django.urls import path
from . import views
from .views import CommentConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/lieu/(?P<event_id>\d+)/comments/$', CommentConsumer.as_asgi()),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('adm', views.admin, name='adm'),
    path('comm/', views.comm, name='comm'),
    
    path('<int:lieu_id>/', views.lieu, name='lieu_detail'),
    path('update-feedback/', views.update_feedback, name='update_feedback'),

    
]
