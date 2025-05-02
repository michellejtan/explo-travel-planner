from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .models import Trip, Itinerary, PackingItem


# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

def about(request):
     contact_details = 'you can reach support at support@catcollector.com' 
     return render(request, 'about.html', {
        'contact': contact_details
    })

def trip_index(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'trips/index.html', {
        'trips': trips
    })
