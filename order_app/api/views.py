# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# 3. Local imports (models)
from order_app.models import Order
from offer_app.models import OfferDetail
# from offers.models import OfferDetail
from .serializers import OrderSerializer


class OrderListCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            customer_user=user
        ) | Order.objects.filter(business_user=user)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new order based on an offer detail.
        Only users of type 'customer' can create orders.
        """
        detail_id = request.data.get("offer_detail_id")
        user = request.user

        if not detail_id:
            return Response({"error": "Missing offer_detail_id."}, status=400)
        if not hasattr(user, "profile") or user.profile.type != "customer":
            return Response({"error": "Permission denied."}, status=403)

        try:
            detail = OfferDetail.objects.select_related("offer").get(id=detail_id)
        except OfferDetail.DoesNotExist:
            return Response(status=404)

        order = Order.objects.create(
            customer_user=user,
            business_user=detail.offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
        )
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=201)

