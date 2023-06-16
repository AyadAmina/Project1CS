from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Favoris, Lieu, User, Evenement, Notification, HistoryEvent, HistoryLieu
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize


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
    print("hello")
    notifications = Notification.objects.all()
    notifications_data = []

    for notification in notifications:
        event = get_object_or_404(Evenement, pk=notification.event_id)
        lieu = get_object_or_404(Lieu, pk=event.lieu_id)
        notification_data = {
            'nomEvent': event.nomEvent,
            'nomLieu': lieu.nomLieu,
        }
        notifications_data.append(notification_data)
    print(notification_data)
    return JsonResponse({'notifications': notifications_data})
 
def History(request):
 if request.method == 'GET':
    HistEvent = HistoryEvent.objects.all()
    HistLieu = HistoryLieu.objects.all()
    History_data = []

    for hist_event in HistEvent:
        event = get_object_or_404(Evenement, pk=hist_event.Idevent.idEvent)
        admin_reg = get_object_or_404(User, pk=hist_event.Iduser.idUser)
        history_data = {
            'Nom': admin_reg.nomUser,
            'Prenom': admin_reg.prenomUser,
            'Action': hist_event.Type_Action,
            'Object': event.nomEvent,
            'Time': hist_event.timestamp
        }
        History_data.append(history_data)

    for hist_lieu in HistLieu:
        lieu = get_object_or_404(Lieu, pk=hist_lieu.Idlieu.idLieu)
        admin_reg = get_object_or_404(User, pk=hist_lieu.Iduser.idUser)
        history_data = {
            'Nom': admin_reg.nomUser,
            'Prenom': admin_reg.prenomUser,
            'Action': hist_lieu.Type_Action,
            'Object': lieu.nomLieu,
            'Time': hist_lieu.timestamp
        }
        History_data.append(history_data)

    print(History_data)
    return render(request, 'Historique.html', {'Histories': History_data})


#---------------------------- Historique des evenments -------------------------------#
#Notifier AdminCentral Ajout Event
def History_Ajout_Event(request, id_event):
 if request.method == 'GET':
    #current_user_id = request.user.id
    event = get_object_or_404(Evenement, pk=id_event)
    user = get_object_or_404(User, pk=1)
    history= HistoryEvent(Iduser=user, Idevent=event, Type_Action="Ajout Evenement")
    history.save()
    return JsonResponse({"message": " added Historyuccessfully."})

#Notifier AdminCentral  Modifier Event
def History_Modifier_Event(request, id_event):
 if request.method == 'POST':
    #current_user_id = request.user.id
    event = get_object_or_404(Evenement, pk=id_event)
    user = get_object_or_404(User, pk=1)
    history= HistoryEvent(Iduser=user, Idevent=event, Type_Action="Modification Evenement")
    history.save()
    return JsonResponse({"message": " added Historyuccessfully."})

#Notifier AdminCentral  Supprimer Event
def History_Supprimer_Event(request, id_event):
 if request.method == 'GET':
    #current_user_id = request.user.id
    event = get_object_or_404(Evenement, pk=id_event)
    user = get_object_or_404(User, pk=1)
    history= HistoryEvent(Iduser=user, Idevent=event, Type_Action="Suppression Evenement")
    history.save()
    return JsonResponse({"message": " added Historyuccessfully."})

#-------------------------------- Historique Lieu ------------------------------------------------------#
#Notifier AdminCentral Ajout Lieu
def History_Ajout_Lieu(request, id_lieu):
 if request.method == 'GET':
    #current_user_id = request.user.id
    lieu = get_object_or_404(Lieu, pk=id_lieu)
    user = get_object_or_404(User, pk=1)
    history= HistoryLieu(Iduser=user, Idlieu=lieu, Type_Action="Ajout lieu")
    history.save()
    return JsonResponse({"message": " added Historyuccessfully."})

#Notifier AdminCentral  Modifier Lieu
def History_Modifier_Lieu(request, id_lieu):
 if request.method == 'GET':
    #current_user_id = request.user.id
    lieu = get_object_or_404(Lieu, pk=id_lieu)
    user = get_object_or_404(User, pk=1)
    history= HistoryLieu(Iduser=user, Idlieu=lieu, Type_Action="Modification lieu")
    history.save()
    return JsonResponse({"message": " added Historyuccessfully."})

#Notifier AdminCentral  Supprimer Lieu
def History_Supprimer_Lieu(request, id_lieu):
 if request.method == 'GET':
    #current_user_id = request.user.id
    lieu = get_object_or_404(Lieu, pk=id_lieu)
    user = get_object_or_404(User, pk=1)
    history=HistoryLieu(Iduser=user, Idlieu=lieu, Type_Action="Suppression lieu")
    history.save()
    return JsonResponse({"message": " added Historyuccessfully."})