# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

# 3. Local imports
from profile_app.models import Profile, CustomerProfile
from .serializers import BusinessProfileSerializer, CustomerProfileSerializer


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
