# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework.permissions import BasePermission, SAFE_METHODS

# 3. Local imports


class IsBusinessUser(BasePermission):
    """
    Allows access only to users whose profile type is 'business'.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user and user.is_authenticated and
            hasattr(user, 'type') and user.type == 'business'
        )


# from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Only the creator of the offer may edit or delete it."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
