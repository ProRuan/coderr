# Third-party suppliers
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBusinessUser(BasePermission):
    """
    Allows access only to users whose profile type is 'business'.
    """

    def has_permission(self, request, view):
        """
        Check user type for 'business'.
        """
        user = request.user
        return (
            user and user.is_authenticated and
            getattr(user, 'type', None) == 'business'
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an offer
    to edit or delete it. Read-only access is allowed for all.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check user to be owner and allow read-only access.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
