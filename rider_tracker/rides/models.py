from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('rider', 'Rider'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Ride(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('en-route', 'En-route'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    rider = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rider_rides')
    driver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='driver_rides')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_datetime = models.DateTimeField()
8

class RideEvent(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='events')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
