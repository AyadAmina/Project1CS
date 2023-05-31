from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login, name='login'),
    path('login/admin/AdminCentralPage/', views.adminCentral_view, name='AdminCentralPage'),
    
    path('login/admin/AdminRegionalPage/<int:user_id>/', views.adminRegional_view, name='AdminRegionalPage'),
    path('login/touriste/<int:user_id>/', views.userpage, name='userpage'),


    path('register/', views.register_touriste, name='register_touriste'),
    #path('forgetPassword/', views.forget_password, name='forget_assword'),

    path('login/admin/AdminRegionalPage/<int:user_id>/AddLieu', views.add_lieu, name='add_lieu'),
    path('login/admin/AdminRegionalPage/<int:user_id>/AddEvenement', views.add_evenement, name='add_evenement'),
    path('login/admin/AdminRegionalPage/<int:user_id>/AddMoyenTransport', views.add_moyen_transport, name='add_moyen_transport'),
    path('login/admin/AdminRegionalPage/<int:user_id>/AddTransport', views.add_transport, name='add_transport'),

   
  
]
