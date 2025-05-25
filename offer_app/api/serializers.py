# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import serializers

# 3. Local imports
from offer_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for both reading & (nested) updating an OfferDetail.
    Uses 'offer_type' as the unique key.
    """
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]


class OfferDetailNestedSerializer(serializers.ModelSerializer):
    """
    Full nested representation for an OfferDetail,
    including 'id' so responses show which record.
    """
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]
        read_only_fields = fields


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Updates top-level Offer fields and nested details by offer_type.
    """
    details = OfferDetailSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        # 1) Update Offer fields
        for attr, val in validated_data.items():
            if attr != 'details':
                setattr(instance, attr, val)
        instance.save()

        # 2) Update nested details by offer_type
        for detail_data in validated_data.get('details', []):
            od = instance.details.get(
                # remove id=49 (just for multi-objects)!!!
                offer_type=detail_data['offer_type'])
            for key, value in detail_data.items():
                setattr(od, key, value)
            od.save()

        return instance


# class OfferDetailNestedSerializer(serializers.ModelSerializer):
#     """
#     Full nested representation for each OfferDetail.
#     Used to return updated detail objects with all fields.
#     """
#     id = serializers.IntegerField(required=False)

#     class Meta:
#         model = OfferDetail
#         fields = [
#             'id',
#             'title',
#             'revisions',
#             'delivery_time_in_days',
#             'price',
#             'features',
#             'offer_type',
#         ]
#         read_only_fields = fields  # make all fields read-only when nested


# class OfferDetailSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required=False)

#     class Meta:
#         model = OfferDetail
#         fields = ['id', 'title', 'revisions',
#                   'delivery_time_in_days', 'price', 'features', 'offer_type']


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


# class OfferUpdateSerializer(serializers.ModelSerializer):
#     details = OfferDetailSerializer(many=True, required=False)

#     class Meta:
#         model = Offer
#         fields = ['title', 'image', 'description', 'details']

#     def update(self, instance, validated_data):
#         details_data = validated_data.pop('details', None)
#         print(f"instance: {instance.id}")
#         test_od = OfferDetail.objects.filter(
#             offer=instance.id, offer_type='basic').get(id=49)
#         print(f"test_od: {test_od}")
#         # test_od_id = test_od.get(id=49)
#         # print(f"test_od_id: {test_od_id}")

#         # Update Pokémon fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         if details_data is not None:
#             existing_details = {
#                 detail.id: detail for detail in instance.details.all()}
#             for detail_data in details_data:
#                 detail_id = detail_data.get('id')
#                 if detail_id and detail_id in existing_details:
#                     detail = existing_details[detail_id]
#                     for attr, value in detail_data.items():
#                         if attr != 'id':
#                             setattr(detail, attr, value)
#                     detail.save()
#                 else:
#                     OfferDetail.objects.create(offer=instance, **detail_data)

#         return instance

#         # details_data = validated_data.pop('details', None)

#         # # Update offer fields
#         # for attr, val in validated_data.items():
#         #     setattr(instance, attr, val)
#         # instance.save()

#         # if details_data is not None:
#         #     existing = {d.id: d for d in instance.details.all()}
#         #     for dd in details_data:
#         #         did = dd.get('id')
#         #         if did and did in existing:
#         #             obj = existing[did]
#         #             for k, v in dd.items():
#         #                 if k != 'id':
#         #                     setattr(obj, k, v)
#         #             obj.save()
#         #         else:
#         #             OfferDetail.objects.create(offer=instance, **dd)
#         #     # Ensure at least 3 details remain
#         #     if instance.details.count() < 3:
#         #         raise serializers.ValidationError(
#         #             "An offer must have at least 3 details."
#         #         )

#         # return instance


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
