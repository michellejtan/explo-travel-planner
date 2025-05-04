from datetime import date
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

ITINERARY_TYPES = (
    ('X', 'Other'),
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
    ('A', 'Activity'),
    ('T', 'Travel'),     # e.g., flights, trains, driving
    ('C', 'Check-in'),   # hotel or accommodation check-in
    ('O', 'Check-out'),  # hotel or accommodation check-out
    ('E', 'Event'),      # e.g., concerts, conferences
    ('F', 'Free Time'),  # unstructured time
    ('M', 'Meeting'),    # business or personal meetings
)


CATEGORY_CHOICES = (
    ('Misc', 'Miscellaneous'),
    ('Clothing', 'Clothing'),
    ('Toiletries', 'Toiletries'),
    ('Electronics', 'Electronics'),
    ('Accessories', 'Accessories'),
    ('Documents', 'Documents'),
    ('Food', 'Food'),
    ('Health', 'Health'),
    ('Gear', 'Gear'),
    ('Baby/Kids', 'Baby/Kids'),
    ('Beach/Pool', 'Beach/Pool'),
    ('Work', 'Work'),
    ('Entertainment', 'Entertainment'),
    ('Camping', 'Camping'),
    ('Winter Gear', 'Winter Gear'),
    ('Fitness', 'Fitness'),
)

CATEGORY_PRIORITY = {
    'Documents': 1,
    'Health': 2,
    'Toiletries': 3,
    'Clothing': 4,
    'Food': 5,
    'Electronics': 6,
    'Accessories': 7,
    'Work': 8,
    'Fitness': 9,
    'Entertainment': 10,
    'Beach/Pool': 11,
    'Camping': 12,
    'Winter Gear': 13,
    'Baby/Kids': 14,
    'Gear': 15,
    'Misc': 16,
}


class PackingItem(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(
        'Category',
        max_length=30, 
        choices=CATEGORY_CHOICES, 
        default=CATEGORY_CHOICES[0][0]
    )
    quantity = models.PositiveIntegerField('Quantity', default=1)

    def __str__(self):
        return f"{self.category}: {self.quantity} X {self.name}"

    def get_absolute_url(self):
        return reverse('packing-detail', kwargs={'pk': self.trip.id})
    
    class Meta:
        ordering = ['category', 'name']

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Trip Name', max_length=100)
    destination = models.CharField('Destination', max_length=255)
    start_date = models.DateField('Start Date')
    end_date = models.DateField('End Date')
    notes = models.TextField('Notes', blank=True, null=True)
    # Optional: many-to-many with packing items
    packing_items = models.ManyToManyField('PackingItem', blank=True)
    
    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1
    
    @property
    def status(self):
        today = date.today()
        if self.end_date < today:
            return 'past'
        elif self.start_date > today:
            return 'upcoming'
        return 'current'
    
    def __str__(self):
        return f"{self.name} to {self.destination}"

    def get_absolute_url(self):
        return reverse('trip-detail', kwargs={'trip_id': self.id})
    
    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date must be before or equal to end date.")
        
    class Meta:
        ordering = ['start_date', 'name']


class Itinerary(models.Model): 
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateField('Itinerary date')
    time = models.TimeField('Time', blank=True, null=True)
    type = models.CharField(
        'Itinerary Type',
        max_length=1,
        choices=ITINERARY_TYPES,
        default=ITINERARY_TYPES[0][0]
    )
    activity = models.CharField('Activity', max_length=255)
    address = models.CharField('Address', max_length=255, blank=True, null=True)  # Optional address
    description = models.TextField('Description', blank=True)
    
    def clean(self):
        if self.trip and self.date:
            if self.date < self.trip.start_date or self.date > self.trip.end_date:
                raise ValidationError("Itinerary date must be within the trip's start and end dates.")
            
    def __str__(self):
        return f"{self.date} - {self.activity}"
    
    class Meta:
        ordering = ['date', 'time']