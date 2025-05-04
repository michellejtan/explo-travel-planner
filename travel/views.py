from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .models import Trip, Itinerary, PackingItem
from datetime import date



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
    today = date.today()
    upcoming_trips = trips.filter(end_date__gte=today).order_by('start_date')
    past_trips = trips.filter(end_date__lt=today).order_by('-start_date')
    return render(request, 'trips/index.html', {
        'upcoming_trips': upcoming_trips,
        'past_trips': past_trips,
    })
