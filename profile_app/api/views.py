# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# 3. Local imports
from profile_app.models import Profile, CustomerProfile
from .serializers import BusinessProfileSerializer, CustomerProfileSerializer, ProfileDetailSerializer, ProfileUpdateSerializer
from .permissions import IsProfileOwner


class ProfileViewSet(viewsets.GenericViewSet):
    """
    Handles GET and PATCH for /api/profile/{pk}/
    """
    queryset = Profile.objects.select_related('user').all()

    def get_permissions(self):
        if self.action == 'partial_update':
            return [IsAuthenticated(), IsProfileOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ProfileUpdateSerializer
        return ProfileDetailSerializer

    def retrieve(self, request, pk=None):
        try:
            profile = self.get_object()
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        try:
            profile = self.get_object()
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, profile)
        serializer = self.get_serializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            detail_serializer = ProfileDetailSerializer(profile)
            return Response(detail_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProfileDetailView(RetrieveAPIView):
#     serializer_class = ProfileDetailSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Profile.objects.select_related('user').all()


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
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(type='business')


class CustomerProfileListView(ListAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerProfile.objects.filter(type='customer')
