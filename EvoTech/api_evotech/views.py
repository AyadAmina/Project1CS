from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.template import loader
from .models import *
from .forms import *

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
    

# Create your views here.
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())




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




def adminCentral_view(request): 
     
  return render(request, "admin_central_page.html")

def adminRegional_view(request, user_id):
  user = User.objects.get( idUser=user_id)

  return render(request, "admin_regional_page.html",{'user': user})

def userpage(request, user_id):
  user = User.objects.get( idUser=user_id)

  return render(request, "userpage.html" ,{'user': user})





def add_lieu(request, user_id):
    admin_region = User.objects.get(idUser=user_id)
    region = Region.objects.get(adminRegion= admin_region)
    communes = Commune.objects.filter(regionC=region)
    
    if request.method == 'POST':
        form = LieuForm(request.POST, communes=communes)
        if form.is_valid():
          lieu = form.save(commit=False)
          
          lieu.adminRegion = admin_region
        
          # still lieu.climat 
          lieu.save()

          return redirect('AdminRegionalPage',user_id)
        
        else : 
          error_message = 'Invalid form , whould you try again ?'
          return render(request, 'page-register.html', {'error_message': error_message})  
    else:
        form = LieuForm(communes=communes)


    communes_choices = [(commune.idCommune, commune.nomCommune) for commune in communes]
    form.fields['commune'].choices = communes_choices

    context = {
       'form': form , 
       'user_id' : user_id
       }
    
    return render(request, 'add_lieu.html', context)




def add_evenement(request, user_id):
    admin_region = User.objects.get(idUser=user_id)
    lieux = Lieu.objects.filter(adminRegion=admin_region)

    if request.method == 'POST':
        form = EvenementForm(request.POST, lieux=lieux)
        if form.is_valid():
            form.save()
            return redirect('AdminRegionalPage',user_id)
    else:
        form = EvenementForm(lieux=lieux)
    
    lieux_choices = [(lieu.idLieu, lieu.nomLieu) for lieu in lieux]
    form.fields['lieu'].choices = lieux_choices
    
    context = {
       'form': form ,
       'user_id' : user_id
       }
    
    return render(request, 'add_evenement.html', context)




def add_transport(request, user_id):
    admin_region = User.objects.get(idUser=user_id)
    lieux = Lieu.objects.filter(adminRegion=admin_region)

    if request.method == 'POST':
        form = TransportForm(request.POST, lieux=lieux)
       
        if form.is_valid():
            form.save()
            return redirect('AdminRegionalPage', user_id)
    else:
        form = TransportForm( lieux=lieux)
      
    lieux_choices = [(lieu.idLieu, lieu.nomLieu) for lieu in lieux]
    form.fields['id_lieu'].choices = lieux_choices


    context = {
       'form': form , 
       'user_id' : user_id
       }
    
    return render(request, 'add_transport.html', context)





