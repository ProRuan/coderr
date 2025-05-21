# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers

# 3. Local imports
from review_app.models import Review
from review_app.api.serializers import ReviewSerializer, ReviewUpdateSerializer
from review_app.api.permissions import IsCustomerProfile, IsReviewer


class ReviewListCreateAPIView(ListCreateAPIView):
    """
    GET: list all reviews (authenticated users only).
    POST: create a review (customers only, one per business user).
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomerProfile]

    def perform_create(self, serializer):
        data = serializer.validated_data
        business = data.get('business_user')
        if business is None:
            raise serializers.ValidationError({
                'business_user': 'This field is required.'
            })
        reviewer = self.request.user
        if Review.objects.filter(business_user=business, reviewer=reviewer).exists():
            raise serializers.ValidationError(
                'You have already reviewed this business user.'
            )
        serializer.save(reviewer=reviewer)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)


# class ReviewListCreateAPIView(ListCreateAPIView):
#     """
#     GET: list all reviews (authenticated).
#     POST: create review for business_user (customers only, one per pair).
#     """
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated, IsCustomerProfile]

#     def perform_create(self, serializer):
#         business = serializer.validated_data['business_user']
#         reviewer = self.request.user
#         if Review.objects.filter(business_user=business, reviewer=reviewer).exists():
#             raise serializers.ValidationError(
#                 "Already reviewed this business.")
#         serializer.save(reviewer=reviewer)

#     def create(self, request, *args, **kwargs):
#         try:
#             return super().create(request, *args, **kwargs)
#         except serializers.ValidationError as e:
#             return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET    /api/reviews/{id}/ → retrieve a review
    PATCH  /api/reviews/{id}/ → update rating/description (reviewer only)
    DELETE /api/reviews/{id}/ → delete review (reviewer only)
    """
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated, IsReviewer]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ReviewUpdateSerializer
        return ReviewSerializer


# # 1. Standard libraries

# # 2. Third-party suppliers
# from rest_framework import status, generics, serializers
# from rest_framework.generics import RetrieveUpdateDestroyAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# # 3. Local imports
# from review_app.models import Review
# from .serializers import ReviewSerializer, ReviewUpdateSerializer
# from .permissions import IsCustomer, IsReviewer


# class ReviewListCreateView(generics.ListCreateAPIView):
#     """
#     GET: list all reviews.
#     POST: create a new review (customer only, one per business_user).
#     """
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated, IsCustomer]

#     def perform_create(self, serializer):
#         # Ensure one review per business_user
#         business = serializer.validated_data['business_user']
#         reviewer = self.request.user
#         if Review.objects.filter(business_user=business, reviewer=reviewer).exists():
#             raise serializers.ValidationError(
#                 "You have already reviewed this business."
#             )
#         serializer.save()

#     def create(self, request, *args, **kwargs):
#         """Handle POST with custom perform_create exceptions."""
#         try:
#             return super().create(request, *args, **kwargs)
#         except serializers.ValidationError as e:
#             return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


# class ReviewDetailView(RetrieveUpdateDestroyAPIView):
#     """
#     GET, PATCH, DELETE for a single Review.
#     Only the reviewer may PATCH or DELETE.
#     """
#     queryset = Review.objects.all()
#     permission_classes = [IsAuthenticated, IsReviewer]

#     def get_serializer_class(self):
#         if self.request.method == 'PATCH':
#             return ReviewUpdateSerializer
#         return ReviewSerializer

#     def patch(self, request, *args, **kwargs):
#         """Partially update rating & description."""
#         try:
#             review = self.get_object()
#         except Review.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = self.get_serializer(
#             review, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *args, **kwargs):
#         """Delete a review if requester is the reviewer."""
#         try:
#             review = self.get_object()
#         except Review.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         self.check_object_permissions(request, review)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
