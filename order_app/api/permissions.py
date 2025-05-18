# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS

# 3. Local imports


class IsBusinessUser(BasePermission):
    """Allows access only to business-type users."""

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'business'
        )


class IsStaffOrReadOnly(BasePermission):
    """Allows DELETE only for staff."""

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return bool(request.user and request.user.is_staff)
        return True
