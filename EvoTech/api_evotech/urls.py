from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('', views.index, name='index'),
    path('about.html/', views.map, name='map'),
    path('contact.html/', views.contact, name='contact'),
]

