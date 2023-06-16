from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.template import loader
from .models import *
from .forms import *

from django.shortcuts import render



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
    

def set_region_side():
  regions = {
    "Nord-Ouest": [13, 46, 31, 27, 22, 20, 29, 48, 2, 38, 14],
    "Nord-Milieu": [42, 44, 26, 17, 51, 9, 16, 35, 15, 6, 34, 10, 28],
    "Nord-Est": [18, 25, 21, 23, 36, 41, 24, 4, 19, 5, 40, 12, 7, 57, 43],
    "Sud-Est": [39, 30, 33, 55, 56],
    "Sud-Ouest": [45, 8, 38, 32, 37, 52],
    "Sud-Milieu": [3, 32, 47, 11, 1, 53, 54, 50, 49, 58]
  }
 
  for i in range(1,59 ):
    region = Region.objects.get(numRegion=i)
    for cote, values in regions.items():
        if i in values:
            region.coteRegion = cote
            break
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
  user = User.objects.get( profile="Admin central")

  if request.method == 'POST':
        # Update the user information 
        user.nomUser = request.POST.get('nomUser')
        user.prenomUser = request.POST.get('prenomUser')
        user.username = request.POST.get('username')

        motdepasse = request.POST.get('motdepasse')
        if motdepasse:
            user.motdepasse = motdepasse

        user.save()

  context = {
        'user': user,
  }

  return render(request, "admin_central_page.html",context)


def adminRegional_view(request, user_id):
  user = User.objects.get( idUser=user_id)
  region = Region.objects.get(adminRegion=user)

  if request.method == 'POST':
        # Update the user information 
        user.nomUser = request.POST.get('nomUser')
        user.prenomUser = request.POST.get('prenomUser')
        user.username = request.POST.get('username')

        motdepasse = request.POST.get('motdepasse')
        if motdepasse:
            user.motdepasse = motdepasse

        user.save()

  context = {
        'user': user,
        'region' : region,
  }

  return render(request, "admin_regional_page.html",context)




def userpage(request, user_id):
  user = User.objects.get( idUser=user_id)
  context = {
        'user': user,
  }
    
  return render(request, "userpage.html" ,context)





import os

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
          selected_transports = request.POST.getlist('transports')
          lieu.transport.set(selected_transports)

          lieu.save()

          save_photos(request,lieu.idLieu,None)
          return redirect('add_lieu',user_id)
        
        else : 
          
          return render(request, 'page-register.html')  
    else:
        form = LieuForm(communes=communes)

    communes_choices = [(commune.idCommune, commune.nomCommune) for commune in communes]
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
  
            save_photos(request,event.lieu.idLieu,event)

            return redirect('add_evenement',user_id)
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





