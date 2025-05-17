# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import serializers

# 3. Local imports
from profile_app.models import Profile, CustomerProfile


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type'
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'uploaded_at', 'type'
        ]
