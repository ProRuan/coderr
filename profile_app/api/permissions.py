# Third-party suppliers
from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """
    Permission to allow only users to edit their own profile.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check a user to be owner of the profile.
        """
        return obj == request.user
