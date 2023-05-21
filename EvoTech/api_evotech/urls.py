from django.urls import path
from . import views
from .views import *
from rest_framework import routers
from django.urls import include

#api urls
router = routers.SimpleRouter()
router.register(r'meteos', views.MeteoViewSet, basename='meteo')
router.register(r'themes', views.ThemeViewSet, basename='theme')
router.register(r'categories', views.CategorieViewSet, basename='categorie')
router.register(r'communes', views.CommuneViewSet, basename='commune')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'regions', views.RegionViewSet, basename='region')
router.register(r'moyentransports', views.MoyenTransportViewSet, basename='moyentransport')
router.register(r'evenements', views.EvenementViewSet, basename='evenement')
router.register(r'lieus', views.LieuViewSet, basename='lieu')
router.register(r'transports', views.TransportViewSet, basename='transport')
router.register(r'photos', views.PhotoViewSet, basename='photo')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/',include(router.urls)),
]   
