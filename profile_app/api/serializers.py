# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import serializers

# 3. Local imports
from auth_app.models import CustomUser
# from profile_app.models import Profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file',
            'location', 'tel', 'description', 'working_hours',
            'type', 'email', 'created_at'
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'location',
            'tel', 'description', 'working_hours', 'email'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if 'email' in user_data:
            instance.user.email = user_data['email']
            instance.user.save()
        instance.save()
        return instance


# class ProfileDetailSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='user.email', read_only=True)

#     class Meta:
#         model = Profile
#         fields = [
#             'user', 'username', 'first_name', 'last_name', 'file',
#             'location', 'tel', 'description', 'working_hours',
#             'type', 'email', 'created_at'
#         ]


# class ProfileUpdateSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='user.email', required=False)

#     class Meta:
#         model = Profile
#         fields = [
#             'first_name', 'last_name', 'location',
#             'tel', 'description', 'working_hours', 'email'
#         ]

#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', {})
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         if 'email' in user_data:
#             instance.user.email = user_data['email']
#             instance.user.save()
#         instance.save()
#         return instance


class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for business user profile data.
    """
    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "first_name", "last_name", "file",
            "location", "tel", "description", "working_hours", "type"
        ]
        read_only_fields = ['id', 'username', 'file', 'type']


class BusinessProfileDetailSerializer(BusinessProfileSerializer):
    """
    Serializer for business user profile data.
    """
    class Meta(BusinessProfileSerializer.Meta):
        fields = BusinessProfileSerializer.Meta.fields + [
            "email", "created_at"
        ]
        read_only_fields = BusinessProfileSerializer.Meta.read_only_fields + [
            'created_at'
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer user profile data.
    """
    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "first_name", "last_name",
            "file", "uploaded_at", "type"
        ]
        read_only_fields = ['id', 'username', 'file', 'type']


class CustomerProfileDetailSerializer(CustomerProfileSerializer):
    """
    Serializer for customer user profile data.
    """
    class Meta(CustomerProfileSerializer.Meta):
        fields = CustomerProfileSerializer.Meta.fields + [
            "created_at"
        ]
        read_only_fields = CustomerProfileSerializer.Meta.read_only_fields + [
            'created_at'
        ]
