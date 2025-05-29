# Third-party suppliers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from .serializers import BaseInfoSerializer
from .services import BaseInfoService


class BaseInfoAPIView(APIView):
    """
    View for retrieving base information.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        data = BaseInfoService.get_info()
        serializer = BaseInfoSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
