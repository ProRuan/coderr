# Third-party suppliers
from rest_framework import serializers

# Local imports
from offer_app.models import Offer, OfferDetail


class OfferDetailNestedSerializer(serializers.ModelSerializer):
    """
    Serializer for nested offer details.
    """
    offer_type = serializers.CharField(required=True)

    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]


class OfferStatsMixin:
    """
    Mixin providing methods to get offer details.
    """

    def get_details(self, obj):
        """
        Get offer details.
        """
        if self.context.get('detailed'):
            return OfferDetailNestedSerializer(obj.details.all(), many=True).data
        return [
            {'id': d.id, 'url': f'/api/offerdetails/{d.id}/'}
            for d in obj.details.all()
        ]

    def get_min_price(self, obj):
        """
        Get offer minimum price.
        """
        qs = obj.details.order_by('price')
        return qs.first().price if qs.exists() else None

    def get_min_delivery_time(self, obj):
        """
        Get offer minimum delivery time.
        """
        qs = obj.details.order_by('delivery_time_in_days')
        return qs.first().delivery_time_in_days if qs.exists() else None


class OfferListSerializer(OfferStatsMixin, serializers.ModelSerializer):
    """
    Serializer for listing offers.
    """
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image',
            'description', 'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_user_details(self, obj):
        """
        Get offer user details.
        """
        u = obj.user
        return {
            'first_name': u.first_name,
            'last_name': u.last_name,
            'username': u.username
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new offer.
    """
    details = OfferDetailNestedSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        """
        Validate offer details.
        """
        if len(value) != 3:
            raise serializers.ValidationError({
                'details': '3 details required.'
            })
        return value

    def create(self, validated_data):
        """
        Create a new offer.
        """
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(
            user=self.context['request'].user, **validated_data
        )
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer


class OfferDetailSerializer(OfferStatsMixin, serializers.ModelSerializer):
    """
    Serializer for offer details.
    """
    details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']


class OfferDetailRetrieveSerializer(OfferStatsMixin, serializers.ModelSerializer):
    """
    Serializer for retrieving offer details.
    """
    user = serializers.IntegerField(source='id', read_only=True)
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image',
            'description', 'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time'
        ]


class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating offer details.
    """
    details = OfferDetailNestedSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        """
        Update an offer.
        """
        self.update_offer_fields(instance, validated_data)
        self.update_offer_detail_fields(
            instance, validated_data.get('details', []))
        return instance

    def update_offer_fields(self, instance, validated_data):
        """
        Update offer fields.
        """
        for attr, val in validated_data.items():
            if attr != 'details':
                setattr(instance, attr, val)
        instance.save()

    def update_offer_detail_fields(self, instance, details_data):
        """
        Update offer detail fields.
        """
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            if not offer_type:
                raise serializers.ValidationError({
                    'offer_type': 'offer_type is required.'
                })
            try:
                detail = instance.details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError({'detail': 'Not found.'})
            for key, value in detail_data.items():
                setattr(detail, key, value)
            detail.save()
