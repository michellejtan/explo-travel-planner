from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('trips/', views.trip_index, name='trip-index'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip-detail'),
    path('trips/create/', views.TripCreate.as_view(), name='trip-create'),
    path('trips/<int:pk>/update/', views.TripUpdate.as_view(), name='trip-update'),
    path('trips/<int:pk>/delete/', views.TripDelete.as_view(), name='trip-delete'),
    path(
        'trips/<int:trip_id>/add-itinerary/', 
        views.add_itinerary, 
        name='add-itinerary'
    ),
    path('itineraries/<int:pk>/update/', views.ItineraryUpdate.as_view(), name='itinerary-update'),
    path('itineraries/<int:pk>/delete/', views.ItineraryDelete.as_view(), name='itinerary-delete'),
]