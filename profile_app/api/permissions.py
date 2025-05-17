# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework.permissions import BasePermission

# 3. Local imports


class IsProfileOwner(BasePermission):
    """
    Allows only profile owners to update their own profile.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# # 1. Standard libraries

# # 2. Third-party suppliers
# from rest_framework.permissions import BasePermission

# # 3. Local imports


# class IsProfileOwner(BasePermission):
#     """
#     Allows access only to the owner of the profile.
#     """

#     def has_object_permission(self, request, view, obj):
#         return obj.user == request.user
