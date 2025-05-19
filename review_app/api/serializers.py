# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import serializers

# 3. Local imports
from review_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for listing and creating reviews."""
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer',
            'rating', 'description',
            'created_at', 'updated_at',
        ]

    def create(self, validated_data):
        # Set reviewer from request user
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)
