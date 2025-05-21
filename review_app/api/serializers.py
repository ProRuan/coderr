# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import serializers

# 3. Local imports
from review_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for listing and creating reviews.
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


# class ReviewSerializer(serializers.ModelSerializer):
#     """Full representation of a review."""
#     class Meta:
#         model = Review
#         fields = [
#             'id', 'business_user', 'reviewer',
#             'rating', 'description',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'business_user',
#                             'reviewer', 'created_at', 'updated_at']


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serializer for PATCH: only rating & description."""
    class Meta:
        model = Review
        fields = ['rating', 'description']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError(
                "Rating must be between 1 and 5.")
        return value


# # 1. Standard libraries

# # 2. Third-party suppliers
# from rest_framework import serializers

# # 3. Local imports
# from review_app.models import Review


# class ReviewSerializer(serializers.ModelSerializer):
#     """Serializer for listing and creating reviews."""
#     reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Review
#         fields = [
#             'id', 'business_user', 'reviewer',
#             'rating', 'description',
#             'created_at', 'updated_at',
#         ]

#     def create(self, validated_data):
#         # Set reviewer from request user
#         validated_data['reviewer'] = self.context['request'].user
#         return super().create(validated_data)


# # class ReviewSerializer(serializers.ModelSerializer):
# #     """Full review representation."""
# #     class Meta:
# #         model = Review
# #         fields = [
# #             'id', 'business_user', 'reviewer',
# #             'rating', 'description',
# #             'created_at', 'updated_at',
# #         ]


# class ReviewUpdateSerializer(serializers.ModelSerializer):
#     """Serializer for PATCH: only rating & description."""
#     class Meta:
#         model = Review
#         fields = ['rating', 'description']

#     def validate_rating(self, value):
#         if not (1 <= value <= 5):
#             raise serializers.ValidationError("Rating must be 1–5.")
#         return value
