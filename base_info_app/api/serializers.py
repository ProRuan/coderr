# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import serializers

# 3. Local imports


class BaseInfoSerializer(serializers.Serializer):
    """Serializer for platform basic statistics."""
    valuation_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_user_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()
