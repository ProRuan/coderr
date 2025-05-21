# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Local imports
from auth_app.models import CustomUser
# from profile_app.models import Profile
from .serializers import BusinessProfileDetailSerializer, BusinessProfileSerializer, CustomerProfileDetailSerializer, CustomerProfileSerializer, ProfileDetailSerializer, ProfileUpdateSerializer
from .permissions import IsProfileOwner


class ProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return None

    def get_serializer_class(self, user):
        """
        Selects serializer based on user type.
        """
        if user.type == 'business':
            return BusinessProfileDetailSerializer
        return CustomerProfileDetailSerializer

    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'Profile not found.'}, status=404)

        serializer_class = self.get_serializer_class(user)
        serializer = serializer_class(user)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'Profile not found.'}, status=404)
        if request.user.pk != user.pk:
            return Response({'detail': 'Forbidden.'}, status=403)
        serializer_class = self.get_serializer_class(user)
        serializer = serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ProfileDetailView(RetrieveAPIView):
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.all()


# class ProfileUpdateView(UpdateAPIView):
#     serializer_class = ProfileUpdateSerializer
#     permission_classes = [IsAuthenticated, IsProfileOwner]

#     def get_queryset(self):
#         return Profile.objects.select_related('user').all()

#     def get_serializer_class(self):
#         if self.request.method == 'PATCH':
#             return ProfileUpdateSerializer
#         return ProfileDetailSerializer


class BusinessProfileListView(ListAPIView):
    """
    Lists all business profiles.
    """
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(type='business')


class CustomerProfileListView(ListAPIView):
    """
    Lists all customer profiles.
    """
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(type='customer')
