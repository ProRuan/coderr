# Third-party suppliers
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class BaseProfileSerializer(serializers.ModelSerializer):
    """
    Base serializer for user profiles.
    """
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = [
            'user', 'username', 'first_name',
            'last_name', 'file'
        ]
        read_only_fields = ['user', 'username']

    def update(self, instance, validated_data):
        """
        Update a user profile.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BusinessProfileListSerializer(BaseProfileSerializer):
    """
    List serializer for business user profiles.
    """
    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields + [
            'location', 'tel', 'description',
            'working_hours', 'type'
        ]
        read_only_fields = BaseProfileSerializer.Meta.read_only_fields + [
            'type'
        ]


class CustomerProfileListSerializer(BaseProfileSerializer):
    """
    List serializer for customer user profiles.
    """
    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields + [
            'uploaded_at', 'type'
        ]
        read_only_fields = BaseProfileSerializer.Meta.read_only_fields + [
            'type'
        ]


class BusinessProfileDetailSerializer(BusinessProfileListSerializer):
    """
    Serializer for retrieving/updating business user profiles.
    """
    class Meta(BusinessProfileListSerializer.Meta):
        fields = BusinessProfileListSerializer.Meta.fields + [
            'email', 'created_at'
        ]


class CustomerProfileDetailSerializer(CustomerProfileListSerializer):
    """
    Serializer for retrieving/updating customer user profiles.
    """
    class Meta(CustomerProfileListSerializer.Meta):
        fields = CustomerProfileListSerializer.Meta.fields + [
            'email', 'created_at'
        ]
