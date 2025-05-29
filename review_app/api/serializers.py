# 1. Third-party suppliers
from rest_framework import serializers

# 2. Local imports
from review_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for listing, creating and updating reviews.
    """
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer',
            'rating', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate_rating(self, value):
        """
        Validate rating being in range (1 til 5).
        """
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5.")
        return value
