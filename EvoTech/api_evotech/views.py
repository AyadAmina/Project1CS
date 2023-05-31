from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Search, Lieu
from .forms import SearchForm
import folium
import geocoder
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext


  


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def contact(request):
    language_code = request.GET.get('language')
    if language_code:
        activate(language_code)
    else:
        language_code = get_language()

    context = {'language_code': language_code}
    return render(request, 'contact.html', context)



def map(request):
    form = SearchForm()

    # Create Map Object
    m = folium.Map(location=[0, 0], zoom_start=15)

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            address = form.save()
            location = geocoder.osm(address.address)
            lat = location.lat
            lng = location.lng
            country = location.country

            if lat is None or lng is None:
                address.delete()
                return HttpResponse('Your address input is invalid')

            m = folium.Map(location=[lat, lng], zoom_start=15)
            folium.Marker([lat, lng], tooltip='Click for more', popup=country).add_to(m)

    lieux = Lieu.objects.all()

    # Add markers for each place
    for lieu in lieux:
        folium.Marker([lieu.latitude, lieu.longitude], tooltip=lieu.nomLieu, popup=lieu.descripLieu, icon=folium.Icon(color='green')).add_to(m)

    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }

    return render(request, 'about.html', context)