# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# 3. Local imports
from offer_app.models import Offer, OfferDetail
from .serializers import OfferListSerializer, OfferCreateSerializer, OfferDetailSerializer, OfferPatchSerializer
from .permissions import IsBusinessUser, IsOwnerOrReadOnly


class OfferPagination(PageNumberPagination):
    page_size = 10


class OfferListCreateAPIView(GenericAPIView):
    """
    GET: paginated list of offers (public).
    POST: create an offer (business users only).
    """
    queryset = Offer.objects.all().prefetch_related('details')
    pagination_class = OfferPagination

    def get_serializer_class(self):
        return OfferCreateSerializer if self.request.method == 'POST' else OfferListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        return [AllowAny()]

    def get(self, request):
        page = self.paginate_queryset(self.get_queryset())
        serializer = OfferListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = OfferCreateSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            offer = serializer.save()
            return Response(OfferCreateSerializer(offer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # 1. Standard libraries
# # none

# # 2. Third-party suppliers
# from rest_framework import status, generics
# from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework.pagination import PageNumberPagination

# # 3. Local imports
# from offer_app.models import Offer, OfferDetail
# from .permissions import IsOwnerOrReadOnly
# from .serializers import OfferDetailSerializer, OfferPatchSerializer, OfferListSerializer, OfferCreateSerializer


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    """GET, PATCH, DELETE for a specific Offer by ID."""

    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs) -> Response:
        """Return the offer with all details."""
        try:
            offer = self.get_object()
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs) -> Response:
        """Update an offer partially with nested details."""
        try:
            offer = self.get_object()
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, offer)
        serializer = OfferPatchSerializer(
            offer, data=request.data, partial=True, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            full_serializer = OfferDetailSerializer(offer)
            return Response(full_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs) -> Response:
        """Delete the offer if the user is the owner."""
        try:
            offer = self.get_object()
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, offer)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferDetailRetrieveAPIView(RetrieveAPIView):
    """
    Returns a specific offer detail by ID.
    No authentication or permissions required.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
