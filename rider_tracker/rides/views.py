from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        queryset = self.model.objects.all()

        if 'status' in self.request.query_params:
            status = self.request.query_params['status']
            queryset = queryset.filter(status=status)
        
        if 'rider_email' in self.request.query_params:
            rider_email = self.request.query_params['rider_email']
            queryset = queryset.filter(rider__email=rider_email)

        return queryset


class RideEventViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = RideEventSerializer
    pagination_class = RideEventPagination
    model = RideEvent

    def get_queryset(self):
        return self.model.objects.all()

