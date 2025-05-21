# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import serializers

# 3. Local imports
from offer_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating offer details."""
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]
        read_only_fields = ['id']


class OfferListSerializer(serializers.ModelSerializer):
    """List serializer with overview data."""
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_details(self, obj):
        return [
            {'id': d.id, 'url': f'/api/offerdetails/{d.id}/'}
            for d in obj.details.all()
        ]

    def get_min_price(self, obj):
        qs = obj.details.order_by('price')
        return qs.first().price if qs.exists() else None

    def get_min_delivery_time(self, obj):
        qs = obj.details.order_by('delivery_time_in_days')
        return qs.first().delivery_time_in_days if qs.exists() else None

    def get_user_details(self, obj):
        u = obj.user
        return {'first_name': u.first_name, 'last_name': u.last_name, 'username': u.username}


class OfferCreateSerializer(serializers.ModelSerializer):
    """Create serializer enforcing ≥3 details."""
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("At least 3 details required.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(
            user=self.context['request'].user, **validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer


# # 1. Standard libraries
# # none

# # 2. Third-party suppliers
# from rest_framework import serializers

# # 3. Local imports
# from offer_app.models import Offer, OfferDetail
# from auth_app.models import CustomUser
# # from django.contrib.auth.models import User


class OfferPatchSerializer(serializers.ModelSerializer):
    """Used only for PATCH (partial update of Offer)."""

    details = OfferDetailSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        """Update offer fields and nested offer details."""
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            for detail_data in details_data:
                detail_id = detail_data.get('id')
                if detail_id:
                    detail = instance.details.get(id=detail_id)
                    for attr, value in detail_data.items():
                        setattr(detail, attr, value)
                    detail.save()
        return instance
