# Third-party suppliers
from django.db.models import Max, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    GenericAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Local imports
from offer_app.api.filters import OfferFilter
from offer_app.models import Offer, OfferDetail
from .paginations import OfferPagination
from .permissions import IsBusinessUser, IsOwnerOrReadOnly
from .serializers import (
    OfferCreateSerializer, OfferDetailNestedSerializer,
    OfferDetailRetrieveSerializer, OfferDetailSerializer,
    OfferDetailUpdateSerializer, OfferListSerializer
)


class OfferListCreateAPIView(GenericAPIView):
    """
    View for listing and creating offers.
    """
    queryset = Offer.objects.all().prefetch_related('details')
    pagination_class = OfferPagination
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
    ]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at']

    def get_queryset(self):
        """
        Get queryset including virtual fields.
        """
        return (
            Offer.objects
                 .annotate(
                     min_price=Min('details__price'),
                     max_delivery_time=Max('details__delivery_time_in_days'),
                 )
            .prefetch_related('details')
        )

    def get_serializer_class(self):
        """
        Get serializer class by request method.
        """
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        """
        Get permissions by request method.
        """
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        return [AllowAny()]

    def get(self, request):
        """
        Get offer list.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Add new offer.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer = serializer.save()
        return Response(
            self.get_serializer(offer).data,
            status=status.HTTP_201_CREATED
        )


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    """
    View for getting, updating and deleting offers.
    """
    queryset = Offer.objects.prefetch_related('details')
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        """
        Get serializer class by request method.
        """
        if self.request.method == 'PATCH':
            return OfferDetailUpdateSerializer
        return OfferDetailRetrieveSerializer

    def get(self, request, *args, **kwargs):
        """
        Get an offer.
        """
        offer = self.get_object()
        serializer = self.get_serializer(offer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        Update an offer.
        """
        offer = self.get_object()
        self.check_object_permissions(request, offer)

        serializer = OfferDetailUpdateSerializer(
            offer, data=request.data,
            partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        offer.refresh_from_db()
        return Response(OfferDetailSerializer(offer, context={'detailed': True}).data)

    def delete(self, request, *args, **kwargs):
        """
        Delete an offer.
        """
        offer = self.get_object()
        self.check_object_permissions(request, offer)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferDetailRetrieveAPIView(RetrieveAPIView):
    """
    View for retrieving offer details.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailNestedSerializer
    permission_classes = [IsAuthenticated]
