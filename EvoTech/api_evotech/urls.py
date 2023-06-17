from django.urls import path, re_path
from . import views
from .views import *
from rest_framework import routers
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .views import map

# api urls
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

websocket_urlpatterns = [
    re_path(r'ws/lieu/(?P<lieu_id>\d+)/comments/$', CommentConsumer.as_asgi()),
]
urlpatterns = [
    path('', views.index, name='index'),
    path('liste_lieux/', views.ListeDesLieux, name='ListeDesLieux'),
    path('détail_lieu/<str:slug>/<int:id>',
         views.LieuDetail, name='LieuDetail'),
    path('liste_event/', views.ListeEvents, name='ListeEvents'),
    path('détail_event/<str:slug>/<int:id>',
         views.EventDetail, name='EventDetail'),
    path('api/suggestionapi/', views.suggestionapi, name='suggestionapi'),
    path('api/suggestionapi2/', views.suggestionapi2, name='suggestionapi2'),
    path('api/', include(router.urls)),

    path('login/', views.login, name='login'),
    path('login/admin/AdminCentralPage/<int:user_id>/',
         views.adminCentral_view, name='AdminCentralPage'),

    path('login/admin/AdminRegionalPage/<int:user_id>/',
         views.adminRegional_view, name='AdminRegionalPage'),
   


    path('register/', views.register_touriste, name='register_touriste'),
     path('logout/<int:user_id>/', views.logout, name='logout'),

    path('login/admin/AdminRegionalPage/<int:user_id>/AddLieu',
         views.add_lieu, name='add_lieu'),
    path('login/admin/AdminRegionalPage/<int:user_id>/AddEvenement',
         views.add_evenement, name='add_evenement'),

    path('login/admin/AdminRegionalPage/<int:user_id>/AddTransport',
         views.add_transport, name='add_transport'),
    path('login/admin/AdminRegionalPage/<int:user_id>/AddProduit', views.add_produit, name='add_produit'),

    path('save-photos/', views.save_photos, name='save_photos'),
    path('statistiques/', views.adminCentral_stats, name='chart'), 


    path('my_profile/<int:user_id>/', views.profile, name='profile'),
    path('delete-favoris/<int:favoris_id>',
         views.delete_favoris, name='delete_favoris'),

    path('notification/<int:admin_id>/', views.adminnot, name='notification'),
    path('comm/', views.comm, name='comm'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('listcomment/<int:admin_id>/', views.listcomment, name='listcomment'),
    path('<int:lieu_id>/', views.lieu, name='lieu_detail'),
    path('update-feedback/', views.update_feedback, name='update_feedback'),
    path('retrieve-feedback/', views.retrieve_feedback, name='retrieve_feedback'),
    path('api/notifications/<int:admin_id>/', views.notification, name='notification'),

    path('map/', views.map, name='map'),
    path('History/', view=views.History, name="Hist"),
    path('Preferable/<int:id_user>/<int:id_lieu>/', views.favorite, name='favorite'),
    path('Notification/<int:id_event>/', views.notification, name='notificaion'),
    path('all_notifications/',view=views.view_notifications,name='all_notifications'),
    path('Histories/Modify/<int:id_event>',views.History_Modifier_Event,name='History_Modifier_Event'),
    path('Histories/Supprimer/<int:id_event>',views.History_Supprimer_Event,name='History_Supprimer_Event'),
    path('Histories/AjoutL/<int:id_lieu>',views.History_Ajout_Lieu,name='History_Ajout_Lieu'),
    path('Histories/ModifierL/<int:id_lieu>',views.History_Modifier_Lieu,name='History_Modifier_Lieu'),
    path('Histories/SupprimerL/<int:id_lieu>',views.History_Supprimer_Lieu,name='History_Supprimer_Lieu'),

    path('login/admin/AdminRegionalPage/<int:user_id>/meslieux/', views.ListeLieuxAdmin, name='ListeLieuxAdmin'),
    path('login/admin/AdminRegionalPage/<int:user_id>/modifier_lieu/<int:lieu_id>', views.update_lieu, name='update_lieu'),
    path('delete-lieu/<int:lieu_id>', views.delete_lieu, name='delete_lieu'),
    path('login/admin/AdminRegionalPage/<int:user_id>/mesevents/', views.ListeEventsAdmin, name='ListeEventsAdmin'),
    path('login/admin/AdminRegionalPage/<int:user_id>/modifier_event/<int:event_id>', views.update_event, name='update_event'),
    path('delete-event/<int:event_id>', views.delete_event, name='delete_event'),
    path('login/admin/AdminRegionalPage/<int:user_id>/mesproduits/', views.ListeProduitsAdmin, name='ListeProduitsAdmin'),
    path('login/admin/AdminRegionalPage/<int:user_id>/modifier_produit/<int:produit_id>', views.update_produit, name='update_produit'),
    path('delete-produit/<int:produit_id>', views.delete_produit, name='delete_produit'),
    path('add_user/',views.addUser , name='addUser'),
    path('liste_comptes/',views.listComptes , name='listComptes'),
    path('delete-user/<int:userId>',views.deleteUser, name='deleteUser'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
