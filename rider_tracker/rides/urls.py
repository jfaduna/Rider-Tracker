from django.urls import path
from .views import RideViewSet, RideEventViewSet, UserViewSet


urlpatterns = [
    # Users
    path('users/', UserViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }), name='user-list'),
    # Rides
    path('rides/', RideViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='ride-list'),
    path('rides/<int:pk>/', RideViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='ride-detail'),
    path('rides/<int:pk>/status/', RideViewSet.as_view({
        'patch': 'update_status',
    }), name='ride-status'),
    # Ride Events
    path('ride-events/', RideEventViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='rideevent-list'),
    path('ride-events/<int:pk>/', RideEventViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='rideevent-detail'),
]
