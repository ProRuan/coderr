from django_filters import rest_framework as filters
from review_app.models import Review


class ReviewFilter(filters.FilterSet):
    business_user_id = filters.NumberFilter(
        field_name='business_user', lookup_expr='exact')
    reviewer_id = filters.NumberFilter(
        field_name='reviewer', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']
