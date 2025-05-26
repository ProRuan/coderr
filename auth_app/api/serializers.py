# Third-party suppliers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    """
    repeated_password = serializers.CharField(
        write_only=True,
        help_text='Repeat the password for verification.'
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password',
            'repeated_password', 'type'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        """
        Ensure both passwords match.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        return data

    def create(self, validated_data):
        """
        Create user with hashed password.
        """
        validated_data.pop('repeated_password')
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        """
        Authenticate with provided credentials.
        """
        user = authenticate(
            username=data['username'], password=data['password']
        )
        if not user:
            raise serializers.ValidationError(
                'Invalid username or password.'
            )
        data['user'] = user
        return data
