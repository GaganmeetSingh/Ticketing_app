from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
    
class City(models.Model):
    city_name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    class Meta:
        unique_together = ('city_name', 'state')

class BusService(models.Model):
    source = models.ForeignKey(City, related_name='bus_service_source', on_delete=models.CASCADE)
    destination = models.ForeignKey(City, related_name='bus_service_destination', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    total_seats = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    departure_time = models.TimeField()
    travel_time = models.TimeField()
    
class Booking(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=50)
    pnr = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # method to generate pnr
    bus_service = models.ForeignKey(BusService, on_delete=models.CASCADE)
    travel_date = models.DateField()
    booking_amount = models.FloatField(null=True)
    seat_number = models.IntegerField(null=True)
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.BinaryField(null=True)
    

    



