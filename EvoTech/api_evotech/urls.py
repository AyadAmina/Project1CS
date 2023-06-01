from django.urls import path, include
from . import views
from .views import Test, favorite, notification , view_notifications


urlpatterns = [
    path('', views.index, name='index'),
    # path('/api', include('CBVapp.urls')),
    path('testing', views.Test, name='Test'),
    path('Preferable/<int:id_user>/<int:id_lieu>/', views.favorite, name='favorite'),
    path('Notification/<int:id_event>/', views.notification, name='notificaion'),
    path('notifications/',view=view_notifications,name='all notifications')
]




