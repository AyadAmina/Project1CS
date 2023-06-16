from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .admin import ProduitsArtisAdmin
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import *
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


import os

#api views
class MeteoViewSet(viewsets.ModelViewSet):
    serializer_class = MeteoSerializer
    queryset = Meteo.objects.all()


class ThemeViewSet(viewsets.ModelViewSet):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()

class CategorieViewSet(viewsets.ModelViewSet):
    serializer_class = CategorieSerializer
    queryset = Categorie.objects.all()

class CommuneViewSet(viewsets.ModelViewSet):
    serializer_class = CommuneSerializer
    queryset = Commune.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class EvenementViewSet(viewsets.ModelViewSet):
    serializer_class = EvenementSerializer
    queryset = Evenement.objects.all()

class LieuViewSet(viewsets.ModelViewSet):
    serializer_class = LieuSerializer
    queryset = Lieu.objects.all()

class TransportViewSet(viewsets.ModelViewSet):
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()

class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


# template views
#home
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

#liste des lieux
product_per_page = 4
def ListeDesLieux(request):
 
  regions = Region.objects.all()
  categories = Categorie.objects.all()
  themes = Theme.objects.all()


  selected_region = request.GET.get('region', "")   
  selected_catg = request.GET.get('categorie', "")   
  selected_thm = request.GET.get('theme', "")
  search= request.GET.get('search', "")

  
  if selected_region:
        lieux = Lieu.objects.filter(region=selected_region).prefetch_related('photos')
        if selected_catg:
            lieux = lieux.filter(categorie=selected_catg).prefetch_related('photos')
        elif selected_thm:
            lieux = lieux.filter(theme=selected_thm).prefetch_related('photos')
        elif search:
            lieux = Lieu.objects.filter(nomLieu__icontains=search).prefetch_related('photos')
  elif selected_catg:
        lieux = Lieu.objects.filter(categorie=selected_catg).prefetch_related('photos')
        if selected_region:
            lieux = lieux.filter(region=selected_region).prefetch_related('photos')
        elif selected_thm:
            lieux = lieux.filter(theme=selected_thm).prefetch_related('photos')
        elif search:
            lieux = Lieu.objects.filter(nomLieu__icontains=search).prefetch_related('photos')
  elif selected_thm:
        lieux = Lieu.objects.filter(theme=selected_thm).prefetch_related('photos')
        if selected_region:
            lieux = lieux.filter(region=selected_region).prefetch_related('photos')
        elif selected_catg:
            lieux = lieux.filter(categorie=selected_catg).prefetch_related('photos')
        elif search:
            lieux = Lieu.objects.filter(nomLieu__icontains=search).prefetch_related('photos')
  elif search:
        lieux = Lieu.objects.filter(nomLieu__icontains=search).prefetch_related('photos')
  else:
        lieux = Lieu.objects.prefetch_related('photos')
 
  #Pagination
  page = request.GET.get('page',1)
  product_paginator = Paginator(lieux, product_per_page)
  try:
      lieux = product_paginator.page(page)
  except EmptyPage:
      lieux = product_paginator.page(product_paginator.num_pages)
  except:
      lieux = product_paginator.page(product_per_page)

  context = { 
      'lieux': lieux,
      'regions': regions,
      'categories' : categories,
      'themes' : themes,
      'page_obj': lieux,
      'is_paginated': True,
      'paginator': product_paginator
      }
   
  return render(request, 'liste_lieux.html', context)
#proposition des recherches
def suggestionapi(request):
    if 'term' in request.GET:
        search = request.GET.get('term')
        qs = Lieu.objects.filter(nomLieu__icontains=search)[0:10]
        titles = list()
        for lieu in qs :
            titles.append(lieu.nomLieu)
        
        return JsonResponse(titles, safe=False)
    return JsonResponse([], safe=False)
#page détail d'un lieu
def LieuDetail(request, slug, id):
  lieu = Lieu.objects.get(idLieu=id)
  events = Evenement.objects.filter(id_lieu=lieu)
  photos = Photo.objects.all()
  transports = lieu.transport.all()
  produits = lieu.produits_artis.all()
  name=request.user.username
  transport_icons = {
        'Métro': 'fa-subway',
        'Bus': 'fa-bus',
        'Taxi': 'fa-taxi',
        'Train': 'fa-train',
        'Tramway': 'fa-train',
        'Téléphérique': 'fa-cable-car',
    }
  transports_with_icons = []
  for transport in transports:
        icon_class = transport_icons.get(transport.typeTrans, '')
        print(icon_class)
        transports_with_icons.append((transport, icon_class))

  context = {
      'lieu': lieu,
      'photos': photos,
      'events': events,
      'transports_with_icons': transports_with_icons,
      'name': name,
      'produits': produits
  }
  return render(request, 'détail_lieu.html', context)

#page liste des événements
def ListeEvents(request):
   
    search= request.GET.get('search', "")
    if search:
        events = Evenement.objects.filter(nomEvent__icontains=search)
    else:
        events = Evenement.objects.all()

    #Pagination
    page = request.GET.get('page',1)
    product_paginator = Paginator(events, product_per_page)
    try:
      events = product_paginator.page(page)
    except EmptyPage:
      events = product_paginator.page(product_paginator.num_pages)
    except:
      events = product_paginator.page(product_per_page)

    context = {
      'events': events,
      'page_obj': events,
      'is_paginated': True,
      'paginator': product_paginator
    }
    return render(request, 'liste_event.html', context)

#proposition des recherches
def suggestionapi2(request):
    if 'term' in request.GET:
        search = request.GET.get('term')
        qs = Evenement.objects.filter(nomEvent__icontains=search)[0:10]
        titles = list()
        for event in qs :
            titles.append(event.nomEvent)
        
        return JsonResponse(titles, safe=False)
    return JsonResponse([], safe=False)

#page détail d'un événement
def EventDetail(request, slug, id):
 event = Evenement.objects.get(idEvent=id)
 lieu = Lieu.objects.get(nomLieu=event.id_lieu)
 lieu_id=event.id_lieu_id
 context = {
      'event': event,
      'lieu': lieu,
      'id_lieu': lieu_id,
    }
 return render(request, 'détail_event.html', context)

#Account treatment
import secrets
from faker import Faker

def create_admin_regional(number_regions):
  fake = Faker()
   
  for i in range(1,number_regions ):
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = f"admin_user{i}"
    password = secrets.token_hex(4)  # Generate a random password
    user = User.objects.create(
        username=username,
        profile="Admin régional",
        nomUser=last_name,
        prenomUser=first_name,
        motdepasse=password
    )
    user.save()


def link_region_adminregional(number_regions):

  for i in range(1,number_regions ):
    region = Region.objects.get(numRegion=i)
    region.adminRegion = User.objects.get(username=f"admin_user{i}")
    region.save()
    


def login(request):
  

  form = LoginForm()
  
  if request.method == 'POST': 
    username = request.POST['username']
    motdepasse = request.POST['motdepasse']
  
    try:
          user = User.objects.get(username=username, motdepasse=motdepasse)
          user_id = user.idUser

          if user.profile=='Admin central' : 
            return redirect('AdminCentralPage')
          
          elif user.profile=='Admin régional' : 
            return redirect('AdminRegionalPage',user_id=user_id)
          
          elif user.profile=='Touriste' : 
            return redirect('userpage',user_id=user_id)
    
    except User.DoesNotExist:
            # User with the given username and password does not exist
            # Handle the case accordingly (e.g., display an error message)
          error_message = 'Invalid username or password, try to register'
          return render(request, 'login.html', {'error_message': error_message})
          
  context = {'form' : form }
  return render(request, "login.html", context)




def register_touriste(request):
  form = RegisterForm()

  if request.method == 'POST': 
      form = RegisterForm(request.POST)

      if form.is_valid():
          username = form.cleaned_data['username']
          nomUser = form.cleaned_data['nomUser']
          prenomUser = form.cleaned_data['prenomUser']
          motdepasse = form.cleaned_data['motdepasse']
            
          # Create the user object and set the default value for the profile field
          user = form.save(commit=False)
          user.profile = 'Touriste'  # Set the default value for the profile field
          user.save()
      else : 
          error_message = 'Invalid form , whould you try again ?'
          return render(request, 'page-register.html', {'error_message': error_message})  
      
  context = {'form' : form }
  return render(request, "page-register.html", context )

# for tests only 

def adminCentral_view(request): 
     
  return render(request, "admin_central_page.html")

def adminRegional_view(request, user_id):
  user = User.objects.get( idUser=user_id)

  return render(request, "admin_regional_page.html",{'user': user})

def userpage(request, user_id):
  user = User.objects.get( idUser=user_id)

  return render(request, "userpage.html" ,{'user': user})



def save_photos(request, lieu ,event):
    if request.method == 'POST' and request.FILES.getlist('images'):
        images = request.FILES.getlist('images')

        for image in images:
            photo = Photo(image=image, lieuId_id=lieu ,eventId=event )
            photo.save()

            # Get the file extension
            _, file_extension = os.path.splitext(image.name)
            # Generate a unique filename using the photoId
            filename = f'photo_{photo.photoId}{file_extension}'

            # Update the image field with the new filename
            photo.image.name = filename
            photo.save()

            # Save the image to the desired location
            with open(os.path.join('static/images', filename), 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)




def add_lieu(request, user_id):
    admin_region = User.objects.get(idUser=user_id)
    region = Region.objects.get(adminRegion=admin_region)
    communes = Commune.objects.filter(regionC=region)
    transports = Transport.objects.all()
    produits_artis = ProduitsArtis.objects.all()
    notification = Notification.objects.filter(adminreg=user_id)

    if request.method == 'POST':
        form = LieuForm(request.POST, communes=communes)

        if form.is_valid():
            lieu = form.save(commit=False)
            lieu.region = region
            lieu.save()
            
            selected_transports = request.POST.getlist('transport')
            lieu.transport.set(selected_transports)

           
            selected_produits = request.POST.getlist('produits_artis')
            lieu.produits_artis.set(selected_produits)

            lieu.save()

            save_photos(request, lieu.idLieu, None)
            return redirect('add_lieu', user_id)
        else:
            print(form.errors)

    else:
        form = LieuForm(communes=communes)

    communes_choices = [(commune.idComm, commune.nomComm) for commune in communes]
    form.fields['commune'].choices = communes_choices

    context = {
        'form': form,
        'user_id': user_id,
        'transports': transports,
        'categories': Categorie.objects.all(),
        'themes': Theme.objects.all(),
        'notification': notification,
        'produits_artis':produits_artis
    }

    return render(request, 'add_lieu.html', context)





def add_evenement(request, user_id):
    admin_region = User.objects.get(idUser=user_id)
    region = Region.objects.get(adminRegion= admin_region)
    lieux = Lieu.objects.filter(region=region)

    if request.method == 'POST':
        form = EvenementForm(request.POST, lieux=lieux)
        if form.is_valid():
            event = form.save()
  
            save_photos(request,event.id_lieu.idLieu,event)

            return redirect('add_evenement',user_id)
    else:
        form = EvenementForm(lieux=lieux)
    
    lieux_choices = [(lieu.idLieu, lieu.nomLieu) for lieu in lieux]
    form.fields['id_lieu'].choices = lieux_choices
    
    context = {
       'form': form ,
       'user_id' : user_id
       

       }
    
    return render(request, 'add_evenement.html', context)




def add_transport(request, user_id):
    if request.method == 'POST':
        form = TransportForm(request.POST)
       
        if form.is_valid():
            form.save()
            return redirect('add_transport', user_id)
    else:
        form = TransportForm( )


    context = {
       'form': form , 
       'user_id' : user_id
       }
    
    return render(request, 'add_transport.html', context)

def add_produit(request, user_id):
    if request.method == 'POST':
        form = ProduitsArtisForm(request.POST)
       
        if form.is_valid():
            form.save()
            return redirect('add_produit', user_id)
    else:
        form = ProduitsArtisForm( )


    context = {
       'form': form , 
       'user_id' : user_id
       }
    
    return render(request, 'add_produit.html', context)


#Profile treatment
def profile(request, id):
    user = User.objects.get(idUser=id)
    lieuxFavoris = Favoris.objects.filter(idUser=id)
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        nom_utilisateur = request.POST.get('nom_utilisateur')
        password = request.POST.get('password')  # Add this line to get the password value
        
        if nom:
            user.nomUser = nom
        if prenom:
            user.prenomUser = prenom
        if nom_utilisateur:
            user.username = nom_utilisateur
        if password:
            user.password = password  # Update the user's password with the new value
        
        user.save()
 
        return redirect('profile', id=id)
    
    return render(request, 'my_profile.html', {'user': user, 'lieuxFavoris': lieuxFavoris})

#suppression
def delete_favoris(request, favoris_id):
    favoris = get_object_or_404(Favoris, id_favoris=favoris_id)
    favoris.delete()
    return HttpResponse(status=204)

#commentaires/feedbacks
class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       
        self.lieu_id = self.scope['url_route']['kwargs']['lieu_id']
        self.lieu_group_name = 'lieu_%s_comments' % self.lieu_id

        # Join lieu group
        await self.channel_layer.group_add(
            self.lieu_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave lieu group
        await self.channel_layer.group_discard(
            self.lieu_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        comment = text_data_json['comment']
        author = text_data_json['author']

        # Save the comment to the database asynchronously
        await database_sync_to_async(Comment.objects.create)(
            lieu_id=self.lieu_id,
            author=author,
            text=comment
        )
        # Create a notification for the admin
        lieu = await database_sync_to_async(Lieu.objects.get)(pk=self.lieu_id)
        admin_id = await database_sync_to_async(lieu.get_admin_id)()
        admin = await database_sync_to_async(User.objects.get)(idUser=admin_id)
        notification =await database_sync_to_async( Notification.objects.create)(adminreg=admin, lieu=lieu.nomLieu,author=author)

        # Send the comment to the lieu group
        await self.channel_layer.group_send(
            self.lieu_group_name,
            {
                'type': 'comment_message',
                'comment': comment,
                'author': author
            }
        )

    async def comment_message(self, lieu):
        # Send the comment to the WebSocket
        await self.send(text_data=json.dumps({
            'comment': lieu['comment'],
            'author': lieu['author']
        }))


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
def admin(request):
    template = loader.get_template('indexadmin.html')
    return HttpResponse(template.render())
def comm(request):
 
    return render(request,'comm.html')

def lieu(request, lieu_id):
    lieu = Lieu.objects.get(pk=lieu_id)
    username = request.user.username
    return render(request, 'comm.html', {'lieu': lieu,'name':username})

def adminnot(request):
    notifications = Notification.objects.filter(adminreg=request.user.id).order_by('-created_at')[:5]  
    template = loader.get_template('indexadmin.html')
    context = {
        'notifications': notifications
    }
    return HttpResponse(template.render(context, request))




class AdminNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['user'].id
        self.admin_notification_group_name = f'admin_notification_{user_id}'

        # Join admin notification group
        await self.channel_layer.group_add(
            self.admin_notification_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave admin notification group
        await self.channel_layer.group_discard(
            self.admin_notification_group_name,
            self.channel_name
        )

    async def send_notification(self, lieu):
        # Send the notification to the WebSocket
        await self.send(text_data=json.dumps({
            'comment': lieu['comment'],
            'author': lieu['author']
        }))





@login_required  # Restrict access to authenticated users
def update_feedback(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        lieu_id = request.POST.get('lieu_id')
        rating = int(request.POST.get('rating'))
        

        try:
            lieu = get_object_or_404(Lieu, idLieu=lieu_id)

            # Check if the user already has a feedback for the lieu
            existing_feedback = Feedback.objects.filter(user=request.user.id, lieu=lieu).first()

            if existing_feedback:
                # If the user has an existing feedback, update it
                existing_feedback.rating = rating
              
                existing_feedback.save()
            else:
                # Create a new feedback instance
                feedback = Feedback(user=request.user.id, lieu=lieu, rating=rating)
                feedback.save()

            # Update the feedback and number of feedback in the Lieu model
            lieu_feedbacks = Feedback.objects.filter(lieu=lieu)
            num_feedbacks = lieu_feedbacks.count()
            total_rating = sum(feedback.rating for feedback in lieu_feedbacks)
            lieu.feedback = total_rating / num_feedbacks if num_feedbacks > 0 else 0
            lieu.nmb_feedback = num_feedbacks
            lieu.save()

            return JsonResponse({'success': True})
        except Lieu.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lieu not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def retrieve_feedback(request):
    
    if request.method == 'POST':
        lieu_id = request.POST.get('lieu_id')
        feedback = Feedback.objects.filter(lieu_id=lieu_id)
        num_feedback = feedback.count()
        total_rating = sum(feedback.values_list('rating', flat=True))
        average_rating = round(total_rating / num_feedback) if num_feedback > 0 else 0

        user_rating = 0
        if request.user.is_authenticated:
            user_feedback = feedback.filter(user=request.user.id)
            if user_feedback.exists():
                user_rating = user_feedback.first().rating

        return JsonResponse({
            'feedback': total_rating,
            'num_feedback': num_feedback,
            'average_rating': average_rating,
            'user_rating': user_rating
        })
    else:
        return JsonResponse({'error': 'Invalid request method'})

#lieux admin
def ListeLieuxAdmin(request, user_id):
   adminR = User.objects.get(idUser=user_id)
   regionR = Region.objects.get(adminRegion=adminR)
   lieux= Lieu.objects.filter(region=regionR)
   context ={
        'lieux': lieux,
        'user_id': user_id
     }
   return render(request, 'meslieux.html', context)

def update_lieu(request, user_id, lieu_id):
    admin_region = User.objects.get(idUser=user_id)
    region = Region.objects.get(adminRegion=admin_region)
    communes = Commune.objects.filter(regionC=region)
    transports = Transport.objects.all()
    notification = Notification.objects.filter(adminreg=user_id)
    produits_artis = ProduitsArtis.objects.all()

    lieu = Lieu.objects.get(idLieu=lieu_id)  # Get the existing lieu object

    if request.method == 'POST':
        form = LieuForm(request.POST, instance=lieu, communes=communes)

        if form.is_valid():
            lieu = form.save(commit=False)
            lieu.region = region
            selected_transports = request.POST.getlist('transport')
            lieu.transport.set(selected_transports)
            selected_produits = request.POST.getlist('produits_artis')
            lieu.produits_artis.set(selected_produits)
            lieu.save()
            save_photos(request, lieu.idLieu, None)
           
            return redirect('update_lieu', user_id, lieu_id)
        else:
            print(form.errors)
    else:
        form = LieuForm(instance=lieu, communes=communes)

    communes_choices = [(commune.idComm, commune.nomComm) for commune in communes]
    form.fields['commune'].choices = communes_choices

    context = {
        'form': form,
        'user_id': user_id,
        'lieu_id': lieu_id,  # Pass the lieu_id to the template
        'transports': transports,
        'categories': Categorie.objects.all(),
        'themes': Theme.objects.all(),
        'notification': notification,
        'lieu': lieu,
        'produits_artis': produits_artis
    }

    return render(request, 'modifier_lieu.html', context)

def delete_lieu(request, lieu_id):
    lieu = get_object_or_404(Lieu, idLieu=lieu_id)
    lieu.delete()
    return HttpResponse(status=204)

#evenements admin
def ListeEventsAdmin(request, user_id):
   adminR = User.objects.get(idUser=user_id)
   regionR = Region.objects.get(adminRegion=adminR)
   lieux= Lieu.objects.filter(region=regionR)
   events= Evenement.objects.filter(id_lieu__in=lieux)
   context ={
        'lieux': lieux,
        'user_id': user_id,
        'events': events
     }
   return render(request, 'mesevents.html', context)

def update_event(request, user_id, event_id):
 
    admin_region = User.objects.get(idUser=user_id)
    region = Region.objects.get(adminRegion= admin_region)
    lieux = Lieu.objects.filter(region=region)
    event = Evenement.objects.get(idEvent=event_id)  # Get the existing event object
    print("objet:",event)
    if request.method == 'POST':
        form = EvenementForm(request.POST, lieux=lieux, instance=event)
        if form.is_valid():
            event = form.save()
            save_photos(request,event.id_lieu.idLieu,event)

            return redirect('update_event',user_id, event_id)
    else:
        form = EvenementForm(lieux=lieux, instance=event)
    
    lieux_choices = [(lieu.idLieu, lieu.nomLieu) for lieu in lieux]
    form.fields['id_lieu'].choices = lieux_choices
    
    context = {
       'form': form ,
       'user_id' : user_id,
       'event_id': event_id,
       'event': event
       

       }
    
    return render(request, 'modifier_event.html', context)

def delete_event(request, event_id):
    event = get_object_or_404(Evenement, idEvent=event_id)
    event.delete()
    return HttpResponse(status=204)

#produits admin
def ListeProduitsAdmin(request, user_id):
   adminR = User.objects.get(idUser=user_id)
   regionR = Region.objects.get(adminRegion=adminR)
   lieux= Lieu.objects.filter(region=regionR)
   produits = ProduitsArtis.objects.filter(lieu__in=lieux)
   context ={
        'lieux': lieux,
        'user_id': user_id,
        'produits': produits
        
     }
   return render(request, 'mesproduits.html', context)

def update_produit(request, user_id, produit_id):
    produit = ProduitsArtis.objects.get(idProduit=produit_id)  # Get the existing produit object

    if request.method == 'POST':
        form = ProduitsArtisForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('update_produit', user_id, produit_id)
    else:
        form = ProduitsArtisForm(instance=produit)

    context = {
        'form': form,
        'user_id': user_id,
        'produit_id': produit_id,
        'produit': produit
    }

    return render(request, 'modifier_produit.html', context)


def delete_produit(request, produit_id):
    produit = get_object_or_404(ProduitsArtis, idProduit=produit_id)
    produit.delete()
    return HttpResponse(status=204)