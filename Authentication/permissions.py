from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    """
    فقط ادمین‌ها یا صاحب شیء می‌توانند دسترسی داشته باشند.
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.role == 'admin':
            return True
        return obj.owner == request.user