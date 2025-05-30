# Third-party suppliers
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from .permissions import IsAdminDelete, IsBusinessUser
from .serializers import (
    CompletedOrderCountSerializer, OrderCountSerializer,
    OrderCreateSerializer, OrderSerializer
)
from offer_app.models import OfferDetail
from order_app.models import Order

User = get_user_model()


class OrderListCreateAPIView(GenericAPIView):
    """
    View for listing and creating orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get queryset of orders created by customer user or business user.
        """
        user = self.request.user
        return (
            Order.objects.filter(customer_user=user)
            | Order.objects.filter(business_user=user)
        )

    def get(self, request):
        """
        Get order list.
        """
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Add new order.
        """
        if request.user.type != 'customer':
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        detail = self.get_offer_detail(
            serializer.validated_data['offer_detail_id'])
        order = self.create_order_from_detail(request.user, detail)
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)

    def get_offer_detail(self, detail_id):
        """
        Get offer detail by id.
        """
        return OfferDetail.objects.select_related('offer').get(id=detail_id)

    def create_order_from_detail(self, user, detail):
        """
        Create an order related to an offer detail.
        """
        return Order.objects.create(
            customer_user=user,
            business_user=detail.offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
        )


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating and deleting orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser, IsAdminDelete]


class OpenOrderCountAPIView(APIView):
    """
    View for counting orders 'in progress'.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Get amount of orders 'in progress'.
        """
        try:
            User.objects.get(pk=business_user_id, type='business')
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='in_progress'
        ).count()
        serializer = OrderCountSerializer({'order_count': count})
        return Response(serializer.data)


class CompletedOrderCountAPIView(APIView):
    """
    View for counting 'completed' orders.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Get amount of 'completed' orders.
        """
        try:
            User.objects.get(pk=business_user_id, type='business')
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='completed'
        ).count()
        serializer = CompletedOrderCountSerializer(
            {'completed_order_count': count})
        return Response(serializer.data)
