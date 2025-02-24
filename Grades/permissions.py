from rest_framework.permissions import BasePermission

class IsAdminUserOnly(BasePermission):
    """
    Custom permission to allow access only to admin users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is an admin
        return request.user and request.user.role == "Admin"
