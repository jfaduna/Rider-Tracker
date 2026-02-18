from rest_framework import serializers
from .models import User, Ride, RideEvent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role'
        ]

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = [
            'id',
            'description',
            'created_at'
        ]

class RideSerializer(serializers.ModelSerializer):
    events = RideEventSerializer(many=True, read_only=True)

    class Meta:
        model = Ride
        fields = '__all__'
        
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

        # Optional: prevent rider and driver being the same user
        if rider == driver:
            raise serializers.ValidationError("Rider and driver cannot be the same user.")

        return data
