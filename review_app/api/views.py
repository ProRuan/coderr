# Third-party suppliers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters, status, serializers

# Local imports
from review_app.api.filters import ReviewFilter
from review_app.api.permissions import IsCustomerProfile, IsReviewer
from review_app.api.serializers import ReviewSerializer
from review_app.api.throttling import ReviewThrottle
from review_app.models import Review


class ReviewListCreateAPIView(ListCreateAPIView):
    """
    View for listing and creating reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomerProfile]
    throttle_classes = [ReviewThrottle]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at', '-rating']

    def perform_create(self, serializer):
        """
        Perform creating a unique review per business user.
        """
        data = serializer.validated_data
        business = data.get('business_user')
        if business is None:
            raise serializers.ValidationError({
                'business_user': 'This field is required.'
            })
        reviewer = self.request.user
        rev = Review.objects.filter(business_user=business, reviewer=reviewer)
        if rev.exists():
            raise serializers.ValidationError({
                'reviewer': 'You already created a review.'
            })
        serializer.save(reviewer=reviewer)

    def create(self, request, *args, **kwargs):
        """
        Add a review.
        """
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating and deleting reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewer]
    throttle_classes = [ReviewThrottle]
