from datetime import timedelta
from django.utils import timezone

from rest_framework import serializers
from .models import User, Ride, RideEvent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
        )
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = [
            'id',
            'ride',
            'description',
            'created_at',
        ]


class UserRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role'
        ]


class RideSerializer(serializers.ModelSerializer):
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            'id',
            'status',
            'rider',
            'driver',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_datetime',
            'todays_ride_events',
        ]
        
    def validate(self, data):
        """
        Ensure the rider has role 'rider' and driver has role 'driver'.
        """
        rider = data.get('rider')
        driver = data.get('driver')

        if rider.role != 'rider':
            raise serializers.ValidationError({'rider': f"User {rider.username} is not a rider."})

        if driver.role != 'driver':
            raise serializers.ValidationError({'driver': f"User {driver.username} is not a driver."})

        # prevent rider and driver being the same user
        if rider == driver:
            raise serializers.ValidationError("Rider and driver cannot be the same user.")

        return data

    def get_todays_ride_events(self, obj):
        if hasattr(obj, "todays_events"):
            return RideEventSerializer(obj.todays_events, many=True).data

        # Fallback for POST request
        last_24h = timezone.now() - timedelta(hours=24)
        queryset = obj.events.filter(created_at__gte=last_24h)
        return RideEventSerializer(queryset, many=True).data
    
    def create(self, validated_data):
        if validated_data.get('status') != 'accepted':
            raise serializers.ValidationError({'status': f"Ride status must be 'accepted' first"})

        instance = super().create(validated_data)
        RideEvent.objects.create(
            ride=instance,
            description="Ride has been Accepted"
        )

        return instance

    def to_representation(self, instance):
        """Customize output to show nested rider and driver info"""
        rep = super().to_representation(instance)
        
        
        if instance.rider:
            rep['rider'] = UserRideSerializer(instance.rider).data

        if instance.driver:
            rep['driver'] = UserRideSerializer(instance.driver).data
        
        return rep

class RideStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["status"]

    def update(self, instance, validated_data):
        new_status = validated_data.pop("status", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # status handled separately
        if new_status and new_status != instance.status:
            instance.change_status(new_status)

        return instance
