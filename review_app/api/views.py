# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import status, generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# 3. Local imports
from review_app.models import Review
from .serializers import ReviewSerializer
from .permissions import IsCustomer


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    GET: list all reviews.
    POST: create a new review (customer only, one per business_user).
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        # Ensure one review per business_user
        business = serializer.validated_data['business_user']
        reviewer = self.request.user
        if Review.objects.filter(business_user=business, reviewer=reviewer).exists():
            raise serializers.ValidationError(
                "You have already reviewed this business."
            )
        serializer.save()

    def create(self, request, *args, **kwargs):
        """Handle POST with custom perform_create exceptions."""
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
