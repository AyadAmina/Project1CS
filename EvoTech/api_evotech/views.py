from django.shortcuts import redirect, render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from api_evotech.models import User,Favoris

from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import *
from .serializers import *
from rest_framework import viewsets

from django.shortcuts import get_object_or_404




#serializers:
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class LieuViewSet(viewsets.ModelViewSet):
    serializer_class = LieuSerializer
    queryset = Lieu.objects.all()
    
class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


# Create your views here.
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())



    
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


def delete_favoris(request, favoris_id):
    favoris = get_object_or_404(Favoris, id_favoris=favoris_id)
    favoris.delete()
    return HttpResponse(status=204)

