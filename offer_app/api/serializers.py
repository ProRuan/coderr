# 1. Standard libraries
# none

# 2. Third-party suppliers
from rest_framework import serializers

# 3. Local imports
from offer_app.models import Offer, OfferDetail
from django.contrib.auth.models import User


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class OfferListSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailSerializer(source='user')

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_details(self, obj):
        return [{"id": d.id, "url": f"/offerdetails/{d.id}/"} for d in obj.details.all()]

    def get_min_price(self, obj):
        return obj.details.order_by('price').first().price if obj.details.exists() else None

    def get_min_delivery_time(self, obj):
        return obj.details.order_by('delivery_time_in_days').first().delivery_time_in_days if obj.details.exists() else None


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "At least 3 offer details are required.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(
            user=self.context['request'].user, **validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer


# # 1. Standard libraries

# # 2. Third-party suppliers
# from rest_framework import serializers

# # 3. Local imports
# from offer_app.models import Offer, OfferDetail
# from django.contrib.auth.models import User


# class OfferDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OfferDetail
#         fields = [
#             'id', 'title', 'revisions', 'delivery_time_in_days',
#             'price', 'features', 'offer_type'
#         ]


# class OfferSerializer(serializers.ModelSerializer):
#     details = OfferDetailSerializer(many=True)
#     min_price = serializers.FloatField(read_only=True)
#     min_delivery_time = serializers.IntegerField(read_only=True)
#     user_details = serializers.SerializerMethodField()

#     class Meta:
#         model = Offer
#         fields = [
#             'id', 'user', 'title', 'image', 'description',
#             'created_at', 'updated_at', 'details',
#             'min_price', 'min_delivery_time', 'user_details'
#         ]

#     def get_user_details(self, obj):
#         user = obj.user
#         return {
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "username": user.username
#         }

#     def create(self, validated_data):
#         details_data = validated_data.pop('details')
#         if len(details_data) < 3:
#             raise serializers.ValidationError(
#                 {"details": "At least 3 offer details are required."}
#             )
#         offer = Offer.objects.create(**validated_data)
#         for detail in details_data:
#             OfferDetail.objects.create(offer=offer, **detail)
#         return offer
