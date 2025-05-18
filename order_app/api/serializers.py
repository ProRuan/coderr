# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import serializers

# 3. Local imports (models)
from order_app.models import Order
from offer_app.models import OfferDetail
# from offers.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title',
            'revisions', 'delivery_time_in_days', 'price',
            'features', 'offer_type', 'status',
            'created_at', 'updated_at'
        ]
