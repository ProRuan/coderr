# Third-party suppliers
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from .permissions import IsProfileOwner
from .serializers import (
    BusinessProfileDetailSerializer,
    BusinessProfileListSerializer,
    CustomerProfileDetailSerializer,
    CustomerProfileListSerializer,
)

User = get_user_model()


class ProfileDetailAPIView(APIView):
    """
    GET /api/profile/{pk}/ → retrieve profile
    PATCH /api/profile/{pk}/ → update own profile
    """
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self, pk):
        """
        Get user object.
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get_serializer_class(self, user):
        """
        Get serializer class by user type.
        """
        return (
            BusinessProfileDetailSerializer
            if user.type == 'business'
            else CustomerProfileDetailSerializer
        )

    def handle_not_found(self):
        """
        Handle the case 'Profile not found'.
        """
        return Response(
            {'detail': 'Profile not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    def handle_forbidden(self):
        """
        Handle the case 'Forbidden'.
        """
        return Response(
            {'detail': 'Forbidden.'},
            status=status.HTTP_403_FORBIDDEN
        )

    def get(self, request, pk):
        """
        Get user details.
        """
        user = self.get_object(pk)
        if not user:
            return self.handle_not_found()

        serializer_class = self.get_serializer_class(user)
        serializer = serializer_class(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Update user details.
        """
        user = self.get_object(pk)
        if not user:
            return self.handle_not_found()
        if request.user.pk != user.pk:
            return self.handle_forbidden()

        serializer_class = self.get_serializer_class(user)
        serializer = serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseProfileListView(ListAPIView):
    """
    Base view for listing user profiles by type.
    """
    permission_classes = [IsAuthenticated]
    user_type = None
    serializer_class = None

    def get_queryset(self):
        """
        Get a queryset by user type.
        """
        return User.objects.filter(type=self.user_type)


class BusinessProfileListView(BaseProfileListView):
    """
    GET /api/profiles/business/
    """
    user_type = 'business'
    serializer_class = BusinessProfileListSerializer


class CustomerProfileListView(BaseProfileListView):
    """
    GET /api/profiles/customer/
    """
    user_type = 'customer'
    serializer_class = CustomerProfileListSerializer
