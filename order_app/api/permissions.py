# Third-party suppliers
from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """
    Allow updating an order for authenticated business users only.
    """

    def has_permission(self, request, view):
        """
        Check user type for being 'business'.
        """
        if request.method != 'PATCH':
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.type == 'business')


class IsAdminDelete(BasePermission):
    """
    Allow deleting an order for admin users (staff) only.
    """

    def has_permission(self, request, view):
        """
        Check user for being admin (staff).
        """
        if request.method != 'DELETE':
            return True
        user = request.user
        return bool(user and user.is_staff)
