# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework.permissions import BasePermission, SAFE_METHODS

# 3. Local imports


class IsCustomerProfile(BasePermission):
    """
    Allows POST only if user.type == 'customer'.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            u = request.user
            return bool(u and u.is_authenticated and u.type == 'customer')
        return True


class IsReviewer(BasePermission):
    """
    Allows read for any authenticated user; only the creator may edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.reviewer == request.user

# # 1. Standard libraries

# # 2. Third-party suppliers
# from rest_framework.permissions import BasePermission

# # 3. Local imports


# class IsCustomer(BasePermission):
#     """Allows only users with customer profile to create."""

#     def has_permission(self, request, view):
#         if request.method == 'POST':
#             return (
#                 request.user.is_authenticated and
#                 hasattr(request.user, 'profile') and
#                 request.user.profile.type == 'customer'
#             )
#         return True


# class IsReviewer(BasePermission):
#     """
#     Allows only the creator (reviewer) of a review to update or delete it.
#     """

#     def has_object_permission(self, request, view, obj):
#         return obj.reviewer == request.user
