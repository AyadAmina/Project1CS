from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import *

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
    region = Region.objects.get(adminRegion= admin_region)
    communes = Commune.objects.filter(regionC=region)
    transports = Transport.objects.all()
    
    if request.method == 'POST':
        form = LieuForm(request.POST, communes=communes)
       
        if form.is_valid():
          
          lieu = form.save(commit=False)
          lieu.region = region
       
          lieu.save()
          selected_transports = request.POST.getlist('transport')
          lieu.transport.set(selected_transports)

          lieu.save()

          save_photos(request,lieu.idLieu,None)
          return redirect('add_lieu',user_id)
        else:
          print(form.errors)
        
         
    else:
        form = LieuForm(communes=communes)

    communes_choices = [(commune.idComm, commune.nomComm) for commune in communes]
    form.fields['commune'].choices = communes_choices

    context = {
       'form': form , 
       'user_id' : user_id ,
       'transports' : transports,
       'categories' : Categorie.objects.all() ,
       'themes' : Theme.objects.all()
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


