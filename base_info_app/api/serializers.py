# Third-party suppliers
from rest_framework import serializers


class BaseInfoSerializer(serializers.Serializer):
    """
    Serializer for base information.
    """
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()
