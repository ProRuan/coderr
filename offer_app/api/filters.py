# Third-party suppliers
from django_filters import rest_framework as filters

# Local imports
from offer_app.models import Offer


class OfferFilter(filters.FilterSet):
    """
    Filter offers by creator_id, min_price or max_delivery_time.
    """
    creator_id = filters.NumberFilter(field_name='user', lookup_expr='exact')
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_delivery_time = filters.NumberFilter(
        field_name='max_delivery_time', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']
