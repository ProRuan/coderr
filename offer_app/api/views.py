# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# 3. Local imports
from offer_app.models import Offer, OfferDetail
from .serializers import OfferListSerializer, OfferCreateSerializer, OfferDetailSerializer, OfferPatchSerializer, OfferUpdateSerializer, OfferDetailNestedSerializer
from .permissions import IsBusinessUser, IsOwnerOrReadOnly


class OfferPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 20


class OfferListCreateAPIView(GenericAPIView):
    """
    GET: paginated list of offers (public).
    POST: create an offer (business users only).
    """
    queryset = Offer.objects.all().prefetch_related('details')
    pagination_class = OfferPagination

    # not working (nest serializer issue)!!!
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['creator_id', 'min_price', 'max_delivery_time']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    odering = ['-updated_at']

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
    """
    GET   /api/offers/{id}/ → overview + detail URLs
    PATCH /api/offers/{id}/ → update fields & nested details by offer_type
    DELETE /api/offers/{id}/ → delete
    """
    queryset = Offer.objects.prefetch_related('details')
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        return OfferUpdateSerializer if self.request.method == 'PATCH' else OfferListSerializer

    def get(self, request, *args, **kwargs):
        offer = self.get_object()
        return Response(OfferListSerializer(offer).data)

    def patch(self, request, *args, **kwargs):
        offer = self.get_object()
        self.check_object_permissions(request, offer)
        serializer = OfferUpdateSerializer(
            offer, data=request.data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # re-fetch from the DB so 'details' reflects updates
        offer = Offer.objects.get(pk=offer.pk)
        # # clear the prefetch cache so details.all() re-queries
        # if hasattr(offer, '_prefetched_objects_cache'):
        #     offer._prefetched_objects_cache.pop('details', None)

        # return full nested details including 'id'
        nested = OfferDetailNestedSerializer(offer.details.all(), many=True)
        return Response({
            'title': offer.title,
            'image': offer.image.url if offer.image else None,
            'description': offer.description,
            'details': nested.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        offer = self.get_object()
        self.check_object_permissions(request, offer)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class OfferDetailView(RetrieveUpdateDestroyAPIView):
#     """
#     GET   /api/offers/{id}/ → overview + detail URLs
#     PATCH /api/offers/{id}/ → update offer + nested details
#     DELETE /api/offers/{id}/ → delete
#     """
#     queryset = Offer.objects.prefetch_related('details')
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

#     def get_serializer_class(self):
#         if self.request.method == 'PATCH':
#             return OfferUpdateSerializer
#         return OfferListSerializer

#     def get(self, request, *args, **kwargs):
#         offer = self.get_object()
#         return Response(self.get_serializer(offer).data)

#     def patch(self, request, *args, **kwargs):
#         offer = self.get_object()
#         self.check_object_permissions(request, offer)
#         serializer = OfferUpdateSerializer(
#             offer, data=request.data, partial=True, context={'request': request}
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # Reload and return full nested details
#         offer.refresh_from_db()
#         nested = OfferDetailNestedSerializer(
#             offer.details.all(), many=True)  # nested serializer?!
#         return Response(
#             {
#                 'title': offer.title,
#                 'image': offer.image.url if offer.image else None,
#                 'description': offer.description,
#                 'details': nested.data
#             },
#             status=status.HTTP_200_OK
#         )

#     def delete(self, request, *args, **kwargs):
#         offer = self.get_object()
#         self.check_object_permissions(request, offer)
#         offer.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class OfferDetailRetrieveAPIView(RetrieveAPIView):
    """
    Returns a specific offer detail by ID.
    No authentication or permissions required.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
