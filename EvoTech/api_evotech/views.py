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
        password = request.POST.get('password')  
        
        if nom:
            user.nomUser = nom
        if prenom:
            user.prenomUser = prenom
        if nom_utilisateur:
            user.username = nom_utilisateur
        if password:
            user.password = password 
        
        user.save()
 
        return redirect('profile', id=id)
    
    return render(request, 'my_profile.html', {'user': user, 'lieuxFavoris': lieuxFavoris})

#delete a lieux from the list of lieuxFavoris
def delete_favoris(request, favoris_id):
    favoris = get_object_or_404(Favoris, id_favoris=favoris_id)
    favoris.delete()
    return HttpResponse(status=204)


def addUser(request):
    user = None
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        nom_utilisateur = request.POST.get('nom_utilisateur')
        password =  nom_utilisateur + '2023' 
        profile = 'Admin régional'
        
        user = User(nomUser = nom, prenomUser = prenom, username = nom_utilisateur, motdepasse = password, profile = profile )
        user.save()
        return redirect('listComptes')

    return render(request, 'add_user.html', {'user': user})

def listComptes(request):
    users = User.objects.filter(profile = 'Admin régional')
    return render(request, 'liste_comptes.html', {'users': users})

def deleteUser(request, userId):
    user = get_object_or_404(User, idUser=userId)
    user.delete()
    return HttpResponse(status=204)