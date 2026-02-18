from datetime import timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.db.models import F, Prefetch
from django.db.models.functions import Power
from django.utils import timezone

from rides.pagination import RideEventPagination, RidePagination, UserPagination
from rides.permissions import IsAdmin
from .models import Ride, RideEvent, User
from .serializers import RideSerializer, RideEventSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer
    pagination_class = UserPagination
    model = User
    
    def get_queryset(self):
        return self.model.objects.all()


class RideViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = RideSerializer
    pagination_class = RidePagination
    model = Ride
    
    def get_queryset(self):
        last_24h = timezone.now() - timedelta(hours=24)
        queryset = Ride.objects.select_related(
            "rider", "driver"
        ).prefetch_related(
            Prefetch(
                "events",
                queryset=RideEvent.objects.filter(created_at__gte=last_24h),
                to_attr="todays_events",
            )
        )
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)

        return queryset

    def filter_queryset(self, queryset):
        if queryset is None:
            queryset = self.model.objects.none()

        status = self.request.query_params.get('status')
        rider_email = self.request.query_params.get('rider_email')

        if status:
            queryset = queryset.filter(status=status)
        if rider_email:
            queryset = queryset.filter(rider__email__icontains=rider_email)

        return queryset

    def sort_queryset(self, queryset):
        if queryset is None:
            queryset = self.model.objects.none()

        sort_by = self.request.query_params.get('sort_by')

        if sort_by == 'pickup_time':
            queryset = queryset.order_by('pickup_datetime')
        elif sort_by == 'distance':
            lat = self.request.query_params.get('lat')
            lng = self.request.query_params.get('lng')
            if lat is not None and lng is not None:
                try:
                    lat = float(lat)
                    lng = float(lng)
                    # Euclidean distance squared for efficient sorting
                    queryset = queryset.annotate(
                        distance=Power(F('pickup_latitude') - lat, 2) + Power(F('pickup_longitude') - lng, 2)
                    ).order_by('distance')
                except ValueError:
                    pass

        return queryset


class RideEventViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = RideEventSerializer
    pagination_class = RideEventPagination
    model = RideEvent

    def get_queryset(self):
        return self.model.objects.all()

