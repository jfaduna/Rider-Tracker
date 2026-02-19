from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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

    VALID_TRANSITIONS = {
        'accepted': ['en-route', 'cancelled'],
        'en-route': ['pickup', 'cancelled'],
        'pickup': ['dropoff', 'cancelled'],
        'dropoff': ['completed'],
        'completed': [],
        'cancelled': [],
    }
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    rider = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rider_rides')
    driver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='driver_rides')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_datetime = models.DateTimeField()

    def change_status(self, new_status):
        old_status = self.status
        allowed = self.VALID_TRANSITIONS.get(old_status, [])

        if new_status not in allowed:
            raise ValidationError(
                f"Invalid status transition from {old_status} to {new_status}"
            )

        self.status = new_status
        self.save(update_fields=["status"])

        RideEvent.objects.create(
            ride=self,
            description=f"status changed from {old_status} to {new_status}"
        )


class RideEvent(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='events')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
