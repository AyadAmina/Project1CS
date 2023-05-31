from django.shortcuts import redirect, render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from EvoTech.api_evotech.models import Favoris

from api_evotech.models import User

# Create your views here.
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())



def profile(request, id):
    user = User.objects.get(idUser=id)
    lieuxFavoris = Favoris.objects.filter(user=user)
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        nom_utilisateur = request.POST.get('nom_utilisateur')
        
        if nom:
            user.nomUser = nom
        if prenom:
            user.prenomUser = prenom
        if nom_utilisateur:
            user.username = nom_utilisateur
        
        user.save()
        # Optionally, you can redirect the user to a success page
        return redirect('profile', id=id)
    
    return render(request, 'my_profile.html', {'user': user, 'lieuxFavoris': lieuxFavoris })

    


