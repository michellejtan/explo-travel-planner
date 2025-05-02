from django.contrib import admin
from .models import Trip, Itinerary, PackingItem

# Register your models here.
admin.site.register([Trip, Itinerary, PackingItem])
