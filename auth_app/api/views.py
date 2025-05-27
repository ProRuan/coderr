# Third-party suppliers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Local imports
from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationView(CreateAPIView):
    """
    View for registering a new user and returning an auth token.
    """
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Validate and save a new user, then generate a token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, provided = Token.objects.get_or_create(user=user)
        return Response({
            'token':    token.key,
            'username': user.username,
            'email':    user.email,
            'user_id':  user.id
        }, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    """
    View for authenticating a user and returning an auth token.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Validate credentials and return token plus user info.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, provided = Token.objects.get_or_create(user=user)
        return Response({
            'token':    token.key,
            'username': user.username,
            'email':    user.email,
            'user_id':  user.id
        }, status=status.HTTP_200_OK)
