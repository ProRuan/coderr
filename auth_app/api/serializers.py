# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# 3. Local imports
from auth_app.models import CustomUser


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        data['user'] = user
        return data
