# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework.permissions import BasePermission

# 3. Local imports


class IsBusinessUser(BasePermission):
    """
    Allows PATCH only for users whose type == 'business'.
    """

    def has_permission(self, request, view):
        if request.method == 'PATCH':
            u = request.user
            return bool(u and u.is_authenticated and u.type == 'business')
        return True


class IsAdminDelete(BasePermission):
    """
    Allows DELETE only for admin (staff) users.
    """

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return bool(request.user and request.user.is_staff)
        return True


# # 1. Standard libraries

# # 2. Third-party suppliers
# from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS

# # 3. Local imports


# class IsBusinessUser(BasePermission):
#     """Allows access only to business-type users."""

#     def has_permission(self, request, view):
#         return (
#             request.user and
#             request.user.is_authenticated and
#             hasattr(request.user, 'type') and
#             request.user.type == 'business'
#         )


# class IsStaffOrReadOnly(BasePermission):
#     """Allows DELETE only for staff."""

#     def has_permission(self, request, view):
#         if request.method == 'DELETE':
#             return bool(request.user and request.user.is_staff)
#         return True
