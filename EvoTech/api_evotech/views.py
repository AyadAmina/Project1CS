from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Search
from .forms import SearchForm
import folium
import geocoder
from django.shortcuts import render, redirect
from django.http import HttpResponse



# Create your views here.
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())


def map(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    
    if lat == None or lng == None:
        address.delete()
        return HttpResponse('You address input is invalid')

    # Create Map Object
    m = folium.Map(location=[lat, lng], zoom_start=15)

    folium.Marker([lat, lng], tooltip='Click for more',
                  popup=country).add_to(m)
    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'about.html', context)