import random
from datetime import timedelta, datetime
from django.utils import timezone
from rides.models import User, Ride, RideEvent


status_event_map = {
    "accepted": "Ride has been Accepted",
    "en-route": "Driver is en-route",
    "pickup": "Rider picked up",
    "dropoff": "Rider dropped off",
    "completed": "Ride completed",
    "cancelled": "Ride cancelled",
}

# Clear old data
RideEvent.objects.all().delete()
Ride.objects.all().delete()
User.objects.all().delete()

# Create Admin
admin = User.objects.create_superuser(
    username="admin",
    password="password",
    email="admin@test.com",
    role="admin"
)

# Realistic driver names
driver_names = [
    ("John", "Carter"),
    ("Tim", "Holland"),
    ("Ethan", "Brooks"),
    ("Jane", "Doe"),
]

drivers = []
for first, last in driver_names:
    drivers.append(
        User.objects.create_user(
            username=f"{first.lower()}.{last.lower()}",
            first_name=first,
            last_name=last,
            password="password",
            role="driver"
        )
    )

# Create riders
riders = []
for i in range(1, 8):
    riders.append(
        User.objects.create_user(
            username=f"rider{i}",
            first_name=f"Rider{i}",
            last_name="User",
            password="password",
            role="rider"
        )
    )

months = ["2024-01", "2024-02", "2024-03", "2024-04"]

for month in months:
    year, month_num = map(int, month.split("-"))

    for driver in drivers:
        # Random rides per driver per month
        ride_count = random.randint(3, 12)

        for i in range(ride_count):
            rider = random.choice(riders)

            pickup_time = timezone.make_aware(
                datetime(year, month_num, random.randint(1, 25), random.randint(6, 20), 0)
            )

            # Random duration - short and long
            duration_minutes = random.choice([30, 45, 55, 70, 90, 120])
            dropoff_time = pickup_time + timedelta(minutes=duration_minutes)

            ride = Ride.objects.create(
                status="completed",
                rider=rider,
                driver=driver,
                pickup_latitude=14.6 + random.random() / 10,
                pickup_longitude=121.0 + random.random() / 10,
                dropoff_latitude=14.5 + random.random() / 10,
                dropoff_longitude=121.1 + random.random() / 10,
                pickup_datetime=pickup_time,
            )

            RideEvent.objects.create(
                ride=ride,
                description=status_event_map["accepted"],
                created_at=pickup_time - timedelta(minutes=10),
            )

            RideEvent.objects.create(
                ride=ride,
                description=status_event_map["en-route"],
                created_at=pickup_time - timedelta(minutes=5),
            )

            RideEvent.objects.create(
                ride=ride,
                description=status_event_map["pickup"],
                created_at=pickup_time,
            )

            RideEvent.objects.create(
                ride=ride,
                description=status_event_map["dropoff"],
                created_at=dropoff_time,
            )

            RideEvent.objects.create(
                ride=ride,
                description=status_event_map["completed"],
                created_at=dropoff_time + timedelta(minutes=3),
            )

print("Data population completed")
