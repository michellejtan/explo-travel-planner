from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .models import Trip, Itinerary, PackingItem
from .forms import ItineraryForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('trip-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


def about(request):
     contact_details = 'you can reach support at support@explo.com' 
     return render(request, 'about.html', {
        'contact': contact_details
    })

@login_required
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

@login_required
def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    packitems_trip_doesnt_have = PackingItem.objects.exclude(id__in = trip.packing_items.all().values_list('id'))

    itinerary_form = ItineraryForm()

    return render(request, 'trips/detail.html', {
        'trip': trip,
        'trip_status': trip.status,
        'itinerary_form': itinerary_form,
        'availabe_items': packitems_trip_doesnt_have,
    })

@login_required
def add_itinerary(request, trip_id):
    form = ItineraryForm(request.POST)
    
    if form.is_valid():
        new_itinerary = form.save(commit=False) 
        new_itinerary.trip_id = trip_id 
        new_itinerary.save() 
        
    return redirect('trip-detail', trip_id)

@login_required
def associate_packitem(request, trip_id, packitem_id):
    Trip.objects.get(id=trip_id).packing_items.add(packitem_id)
    return redirect('trip-detail', trip_id=trip_id)

@login_required
def remove_packitem(request, trip_id, packitem_id):
    trip = Trip.objects.get(id=trip_id)
    packitem = PackingItem.objects.get(id=packitem_id)
    trip.packing_items.remove(packitem)
    return redirect('trip-detail', trip_id=trip_id)

class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['name', 'destination', 'start_date', 'end_date', 'notes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TripUpdate(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = ['name', 'destination', 'start_date', 'end_date', 'notes']

class TripDelete(LoginRequiredMixin, DeleteView):
    model = Trip
    success_url = '/trips/'

class ItineraryUpdate(LoginRequiredMixin, UpdateView):
    model = Itinerary
    fields = ['date', 'time', 'type', 'activity', 'address', 'description']    
    
    def get_success_url(self):
        return reverse_lazy('trip-detail', kwargs={'trip_id': self.object.trip.id})
    
class ItineraryDelete(LoginRequiredMixin, DeleteView):
    model = Itinerary
    
    def get_success_url(self):
        return reverse_lazy('trip-detail', kwargs={'trip_id': self.object.trip.id})

class PackItemCreate(LoginRequiredMixin, CreateView):
    model = PackingItem
    fields = '__all__'

class PackingItemList(LoginRequiredMixin, ListView):
    model = PackingItem

class PackingItemDetail(LoginRequiredMixin, DetailView):
    model = PackingItem

class PackingItemUpdate(LoginRequiredMixin, UpdateView):
    model = PackingItem
    fields = '__all__'

class PackingItemDelete(LoginRequiredMixin, DeleteView):
    model = PackingItem
    success_url = '/packitems/'