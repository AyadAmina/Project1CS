from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def profile(request):
  template = loader.get_template('my_profile.html')
  return HttpResponse(template.render())
