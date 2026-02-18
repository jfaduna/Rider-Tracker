from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Ride, RideEvent


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )
    list_display = ('id', 'first_name', 'last_name', 'email', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('first_name', 'last_name', 'email',)
    ordering = ('id',)


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
        'rider',
        'driver',
        'pickup_datetime',
    )
    list_filter = ('status', 'pickup_datetime')
    search_fields = ('rider__username', 'driver__username')


@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'ride', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('ride__id', 'description')
    ordering = ('-created_at',)
