# Third-party suppliers
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerProfile(BasePermission):
    """
    Allows only customer users to create reviews.
    """

    def has_permission(self, request, view):
        """
        Check user having permission to create a review.
        """
        if request.method == 'POST':
            u = request.user
            return bool(u and u.is_authenticated and u.type == 'customer')
        return True


class IsReviewer(BasePermission):
    """
    Allows authenticated user to read and creator to edit/delete review.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check user for permission handling reviews.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.reviewer == request.user
