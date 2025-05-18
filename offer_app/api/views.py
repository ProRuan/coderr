# 1. Standard libraries
# none

# 2. Third-party suppliers
from rest_framework import status, generics
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# 3. Local imports
from offer_app.models import Offer, OfferDetail
from .permissions import IsOwnerOrReadOnly
from .serializers import OfferDetailSerializer, OfferPatchSerializer, OfferListSerializer, OfferCreateSerializer


class OfferPagination(PageNumberPagination):
    page_size = 10


class OfferListCreateAPIView(generics.GenericAPIView):
    queryset = Offer.objects.all().prefetch_related('details', 'user')
    permission_classes = [AllowAny]
    pagination_class = OfferPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def get(self, request):
        """List offers with pagination, details, min_price, and min_delivery_time."""
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        """Create offer with at least 3 details. Requires authenticated business user."""
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=401)
        if not hasattr(request.user, 'profile') or request.user.profile.type != 'business':
            return Response({"detail": "Business profile required."}, status=403)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            offer = serializer.save()
            response = OfferCreateSerializer(offer).data
            return Response(response, status=201)
        return Response(serializer.errors, status=400)


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

    def get(self, request, *args, **kwargs):
        try:
            detail = self.get_object()
        except OfferDetail.DoesNotExist:
            return Response(
                {"detail": "Offer detail not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(detail)
        return Response(serializer.data, status=status.HTTP_200_OK)


# # 1. Standard libraries

# # 2. Third-party suppliers
# from rest_framework import status, generics
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from django.db.models import Q

# # 3. Local imports
# from offer_app.models import Offer
# from .serializers import OfferSerializer


# class OfferListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = OfferSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         queryset = Offer.objects.all()

#         # Filtering
#         creator_id = self.request.query_params.get('creator_id')
#         min_price = self.request.query_params.get('min_price')
#         max_delivery = self.request.query_params.get('max_delivery_time')
#         search = self.request.query_params.get('search')
#         ordering = self.request.query_params.get('ordering')

#         if creator_id:
#             queryset = queryset.filter(user_id=creator_id)
#         if min_price:
#             queryset = [
#                 o for o in queryset if o.min_price and o.min_price >= float(min_price)]
#         if max_delivery:
#             queryset = [
#                 o for o in queryset if o.min_delivery_time and o.min_delivery_time <= int(max_delivery)]
#         if search:
#             queryset = queryset.filter(
#                 Q(title__icontains=search) | Q(description__icontains=search))
#         if ordering in ['updated_at', 'min_price']:
#             queryset = sorted(queryset, key=lambda x: getattr(x, ordering))

#         return queryset

#     def post(self, request, *args, **kwargs):
#         # Only business users allowed
#         if not request.user.is_authenticated:
#             return Response({"detail": "Authentication required."}, status=401)
#         if getattr(request.user, 'userprofile', None) and request.user.userprofile.type != 'business':
#             return Response({"detail": "Only business users can post offers."}, status=403)

#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
