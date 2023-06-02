from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Favoris, Lieu, User, Evenement, Notification 
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())


# Function for testing 
def Test(request):

    if request.method == 'GET':
        return JsonResponse({"message": "salaam"})

# Ajouter favorite  
def favorite(request, id_user, id_lieu):
    if request.method == 'POST':
        lieu = get_object_or_404(Lieu, pk=id_lieu)
        uuser = get_object_or_404(User, pk=id_user)
        fav = Favoris(idLieu=lieu, user=uuser)
        fav.save()
        return JsonResponse({"message": "Favorite added successfully."})



#Envoyer notification 
def notification(request, id_event):
    if request.method == 'GET':
        event = get_object_or_404(Evenement, pk=id_event)
        lieu = get_object_or_404(Lieu, pk=event.lieu.idLieu)
        print(lieu) 
        users = User.objects.all()
        for user in users:
            existing_notification = Notification.objects.filter(user=user, event=event, seen=True).exists()
            if not existing_notification:
                notification = Notification.objects.create(user=user, event=event)
        
       
        return render(request, 'notifications.html', {'event':event, 'lieu':lieu})
        
    
    return HttpResponse('Invalid request method.')

#Afficher toutes les notifications 
def view_notifications(request):
   # notifications = Notification.objects.filter(pk=request.user.id)
    notifications = Notification.objects.all()
    return render(request, 'notifications.html', {'notifications': notifications})
