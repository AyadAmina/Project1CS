from django.urls import path
from . import views
from .views import *
from rest_framework import routers
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

#api urls
router = routers.SimpleRouter()
router.register(r'meteos', views.MeteoViewSet, basename='meteo')
router.register(r'themes', views.ThemeViewSet, basename='theme')
router.register(r'categories', views.CategorieViewSet, basename='categorie')
router.register(r'communes', views.CommuneViewSet, basename='commune')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'regions', views.RegionViewSet, basename='region')
router.register(r'evenements', views.EvenementViewSet, basename='evenement')
router.register(r'lieus', views.LieuViewSet, basename='lieu')
router.register(r'transports', views.TransportViewSet, basename='transport')
router.register(r'photos', views.PhotoViewSet, basename='photo')

urlpatterns = [
    path('', views.index, name='index'),
    path('liste_lieux/', views.ListeDesLieux, name='ListeDesLieux'),
    path('détail_lieu/<str:slug>/<int:id>', views.LieuDetail, name='LieuDetail'),
    path('liste_event/', views.ListeEvents, name='ListeEvents'),
    path('détail_event/<str:slug>/<int:id>', views.EventDetail, name='EventDetail'),
    path('api/suggestionapi/', views.suggestionapi, name='suggestionapi'),
    path('api/suggestionapi2/', views.suggestionapi2, name='suggestionapi2'),
    path('api/',include(router.urls)),

    path('login/', views.login, name='login'),
    path('login/admin/AdminCentralPage/', views.adminCentral_view, name='AdminCentralPage'),
    
    path('login/admin/AdminRegionalPage/<int:user_id>/', views.adminRegional_view, name='AdminRegionalPage'),
    path('login/touriste/<int:user_id>/', views.userpage, name='userpage'),


    path('register/', views.register_touriste, name='register_touriste'),

    path('login/admin/AdminRegionalPage/<int:user_id>/AddLieu', views.add_lieu, name='add_lieu'),
    path('login/admin/AdminRegionalPage/<int:user_id>/AddEvenement', views.add_evenement, name='add_evenement'),
    
    path('login/admin/AdminRegionalPage/<int:user_id>/AddTransport', views.add_transport, name='add_transport'),

    path('save-photos/', views.save_photos, name='save_photos'),
    
]  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)