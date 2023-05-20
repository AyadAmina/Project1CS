from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from .serializers import *
from rest_framework import viewsets

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

class MoyenTransportViewSet(viewsets.ModelViewSet):
    serializer_class = MoyenTransportSerializer
    queryset = MoyenTransport.objects.all()

class EvenementViewSet(viewsets.ModelViewSet):
    serializer_class = EvenementSerializer
    queryset = Evenement.objects.all()

class LieuViewSet(viewsets.ModelViewSet):
    serializer_class = LieuSerializer
    queryset = Lieu.objects.all()

class TransportViewSet(viewsets.ModelViewSet):
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()



# template views
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())
