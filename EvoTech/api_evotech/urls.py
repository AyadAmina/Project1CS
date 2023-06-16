from django.urls import path, include
from . import views
from .views import Test, favorite, notification , view_notifications , History_Ajout_Event, History_Modifier_Event,History_Supprimer_Event, History_Supprimer_Lieu, History_Modifier_Lieu,History_Ajout_Lieu


urlpatterns = [
    path('', views.index, name='index'),
    # path('/api', include('CBVapp.urls')),
    path('testing', views.Test, name='Test'),
    path('Hist/',view=views.Hist,name="Hist"),
    path('Preferable/<int:id_user>/<int:id_lieu>/', views.favorite, name='favorite'),
    path('Notification/<int:id_event>/', views.notification, name='notificaion'),
    path('all_notifications/',view=views.view_notifications,name='all_notifications'),
    path('Histories/Modify/<int:id_event>',views.History_Modifier_Event,name='History_Modifier_Event'),
    path('Histories/Supprimer/<int:id_event>',views.History_Supprimer_Event,name='History_Supprimer_Event'),
    path('Histories/AjoutL/<int:id_lieu>',views.History_Ajout_Lieu,name='History_Ajout_Lieu'),
    path('Histories/ModifierL/<int:id_lieu>',views.History_Modifier_Lieu,name='History_Modifier_Lieu'),
    path('Histories/SupprimerL/<int:id_lieu>',views.History_Supprimer_Lieu,name='History_Supprimer_Lieu')
]




