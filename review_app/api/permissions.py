# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework.permissions import BasePermission

# 3. Local imports


class IsCustomer(BasePermission):
    """Allows only users with customer profile to create."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return (
                request.user.is_authenticated and
                hasattr(request.user, 'profile') and
                request.user.profile.type == 'customer'
            )
        return True
