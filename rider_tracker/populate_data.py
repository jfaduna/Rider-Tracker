import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# -----------------------------
# Setup Django environment
# -----------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rider_tracker.settings")  # replace with your settings
django.setup()

from rides.models import User, Ride, RideEvent

# -----------------------------
# Create Riders
# -----------------------------
riders = []
for i in range(1, 6):
    user, created = User.objects.get_or_create(
        username=f'rider{i}',
        defaults={
            'email': f'rider{i}@example.com',
            'role': 'rider',
            'first_name': f'Rider{i}',
            'last_name': 'Test',
            'password': make_password('riderpass123')
        }
    )
    riders.append(user)

# -----------------------------
# Create Drivers
# -----------------------------
drivers = []
for i in range(1, 6):
    user, created = User.objects.get_or_create(
        username=f'driver{i}',
        defaults={
            'email': f'driver{i}@example.com',
            'role': 'driver',
            'first_name': f'Driver{i}',
            'last_name': 'Test',
            'password': make_password('driverpass123')
        }
    )
    drivers.append(user)

# -----------------------------
# Create 10 Rides
# -----------------------------
rides = []
for i in range(10):
    rider = random.choice(riders)
    driver = random.choice(drivers)
    pickup_lat = 6.5 + random.uniform(0, 0.05)
    pickup_lng = 3.37 + random.uniform(0, 0.05)
    dropoff_lat = 6.55 + random.uniform(0, 0.05)
    dropoff_lng = 3.40 + random.uniform(0, 0.05)
    pickup_time = timezone.now() + timedelta(hours=random.randint(-24, 24))
    status = random.choice(['accepted', 'en-route', 'completed', 'cancelled', 'pickup', 'dropoff'])

    ride, created = Ride.objects.get_or_create(
        rider=rider,
        driver=driver,
        pickup_latitude=pickup_lat,
        pickup_longitude=pickup_lng,
        dropoff_latitude=dropoff_lat,
        dropoff_longitude=dropoff_lng,
        pickup_datetime=pickup_time,
        status=status
    )
    rides.append(ride)

# -----------------------------
# Create RideEvents
# -----------------------------
for ride in rides:
    for j in range(random.randint(1, 3)):
        RideEvent.objects.get_or_create(
            ride=ride,
            description=f'Event {j+1} for ride {ride.id}',
        )

print("Sample data populated successfully!")
