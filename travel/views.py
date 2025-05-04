from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
    current_trips = trips.filter(start_date__lte=today, end_date__gte=today).order_by('start_date')
    past_trips = trips.filter(end_date__lt=today).order_by('-start_date')
    return render(request, 'trips/index.html', {
        'upcoming_trips': upcoming_trips,
        'past_trips': past_trips,
        'current_trips': current_trips,
    })

def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', {
        'trip': trip,
        'trip_status': trip.status,
    })

class TripCreate(CreateView):
    model = Trip
    fields = ['name', 'destination', 'start_date', 'end_date', 'notes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TripUpdate(UpdateView):
    model = Trip
    fields = ['name', 'destination', 'start_date', 'end_date', 'notes']

class TripDelete(DeleteView):
    model = Trip
    success_url = '/trips/'