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


class OrderStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating only the order status."""
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        if value not in ('in_progress', 'completed', 'cancelled'):
            raise serializers.ValidationError("Invalid status.")
        return value


class OrderCountSerializer(serializers.Serializer):
    """Serializer for returning the count of open orders."""
    order_count = serializers.IntegerField(default=0)


class CompletedOrderCountSerializer(serializers.Serializer):
    """Serializer for returning the count of completed orders."""
    completed_order_count = serializers.IntegerField()


class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for updating only the 'status' field of an Order.
    """
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        allowed = ('in_progress', 'completed', 'cancelled')
        if value not in allowed:
            raise serializers.ValidationError(
                f"Status must be one of {allowed}.")
        return value


class OrderCountSerializer(serializers.Serializer):
    """
    Serializer for returning the count of open orders.
    """
    order_count = serializers.IntegerField()


class CompletedOrderCountSerializer(serializers.Serializer):
    """
    Serializer for returning the count of completed orders.
    """
    completed_order_count = serializers.IntegerField()


# # 1. Standard libraries

# # 2. Third-party suppliers
# from rest_framework import serializers

# # 3. Local imports (models)
# from order_app.models import Order
# from offer_app.models import OfferDetail
# # from offers.models import OfferDetail


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = [
#             'id', 'customer_user', 'business_user', 'title',
#             'revisions', 'delivery_time_in_days', 'price',
#             'features', 'offer_type', 'status',
#             'created_at', 'updated_at'
#         ]


# class OrderStatusSerializer(serializers.ModelSerializer):
#     """Serializer for updating only the order status."""
#     class Meta:
#         model = Order
#         fields = ['status']

#     def validate_status(self, value):
#         if value not in ('in_progress', 'completed', 'cancelled'):
#             raise serializers.ValidationError("Invalid status.")
#         return value


# class OrderCountSerializer(serializers.Serializer):
#     """Serializer for returning the count of open orders."""
#     order_count = serializers.IntegerField(default=0)


# class CompletedOrderCountSerializer(serializers.Serializer):
#     """Serializer for returning the count of completed orders."""
#     completed_order_count = serializers.IntegerField()
