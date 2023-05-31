from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
