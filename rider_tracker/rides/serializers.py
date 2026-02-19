from rest_framework import serializers
from .models import User, Ride, RideEvent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
        ]
        
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

class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
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
        return RideEventSerializer(obj.todays_events, many=True).data

    def update(self, instance, validated_data):
        new_status = validated_data.pop("status", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # status handled separately
        if new_status and new_status != instance.status:
            instance.change_status(new_status)

        return instance
