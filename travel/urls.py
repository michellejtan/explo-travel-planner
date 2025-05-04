from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('trips/', views.trip_index, name='trip-index'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip-detail'),
    path('catripsts/create/', views.TripCreate.as_view(), name='trip-create'),

]