# Third-party suppliers
from rest_framework import serializers

# Local imports
from offer_app.models import OfferDetail
from order_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for orders.
    """
    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title',
            'revisions', 'delivery_time_in_days', 'price',
            'features', 'offer_type', 'status',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer for creating orders with offer_detail_id validation.
    """
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        """
        Check for offer_detail_id being existent.
        """
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError({
                'offer_detail': 'OfferDetail with this ID does not exist.'
            })
        return value


class OrderCountSerializer(serializers.Serializer):
    """
    Serializer for counting in-progress orders.
    """
    order_count = serializers.IntegerField()


class CompletedOrderCountSerializer(serializers.Serializer):
    """
    Serializer for counting completed orders.
    """
    completed_order_count = serializers.IntegerField()
