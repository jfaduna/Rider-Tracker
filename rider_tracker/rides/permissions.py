from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Invalid user role. Admin access only."
    
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )
