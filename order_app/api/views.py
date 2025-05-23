# 1. Standard libraries

# 2. Third-party suppliers
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# 3. Local imports
from order_app.models import Order
from offer_app.models import OfferDetail
from .serializers import CompletedOrderCountSerializer, OrderSerializer, OrderStatusSerializer, OrderCountSerializer
from .permissions import IsAdminDelete, IsBusinessUser


User = get_user_model()


class OrderListCreateAPIView(GenericAPIView):
    """
    GET: list orders for the authenticated user (as customer or business).
    POST: create an order from an offer detail (customers only).
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        return Order.objects.filter(customer_user=u) | Order.objects.filter(business_user=u)

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        u = request.user
        oid = request.data.get('offer_detail_id')
        if not oid or u.type != 'customer':
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            d = OfferDetail.objects.select_related('offer').get(id=oid)
        except OfferDetail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order = Order.objects.create(
            customer_user=u,
            business_user=d.offer.user,
            title=d.title,
            revisions=d.revisions,
            delivery_time_in_days=d.delivery_time_in_days,
            price=d.price,
            features=d.features,
            offer_type=d.offer_type,
            status='in_progress'
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET    /api/orders/{id}/  → retrieve full order
    PATCH  /api/orders/{id}/  → update status (business only)
    DELETE /api/orders/{id}/  → delete order (admin only)
    """
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsBusinessUser, IsAdminDelete]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OrderStatusSerializer
        return OrderSerializer

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        try:
            return super().patch(request, *args, **kwargs)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class OpenOrderCountAPIView(APIView):
    """
    GET /api/order-count/{business_user_id}/
    Returns the number of 'in_progress' orders for that business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            User.objects.get(pk=business_user_id, type='business')
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='in_progress'
        ).count()

        serializer = OrderCountSerializer({'order_count': count})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompletedOrderCountAPIView(APIView):
    """
    GET /api/completed-order-count/{business_user_id}/
    Returns the number of 'completed' orders for that business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        # Verify business user exists
        try:
            User.objects.get(pk=business_user_id, type='business')
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Count completed orders
        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='completed'
        ).count()

        # Serialize and return
        serializer = CompletedOrderCountSerializer(
            {'completed_order_count': count})
        return Response(serializer.data, status=status.HTTP_200_OK)


# # 1. Standard libraries

# # 2. Third-party suppliers
# from django.contrib.auth.models import User
# from rest_framework import status
# from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView

# # 3. Local imports (models)
# from order_app.models import Order
# from offer_app.models import OfferDetail
# # from offers.models import OfferDetail
# from .permissions import IsBusinessUser, IsStaffOrReadOnly
# from .serializers import CompletedOrderCountSerializer, OrderCountSerializer, OrderSerializer, OrderStatusSerializer


# class OrderListCreateView(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Order.objects.filter(
#             customer_user=user
#         ) | Order.objects.filter(business_user=user)

#     def get(self, request):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """
#         Create a new order based on an offer detail.
#         Only users of type 'customer' can create orders.
#         """
#         detail_id = request.data.get("offer_detail_id")
#         user = request.user

#         if not detail_id:
#             return Response({"error": "Missing offer_detail_id."}, status=400)
#         if not hasattr(user, "profile") or user.profile.type != "customer":
#             return Response({"error": "Permission denied."}, status=403)

#         try:
#             detail = OfferDetail.objects.select_related(
#                 "offer").get(id=detail_id)
#         except OfferDetail.DoesNotExist:
#             return Response(status=404)

#         order = Order.objects.create(
#             customer_user=user,
#             business_user=detail.offer.user,
#             title=detail.title,
#             revisions=detail.revisions,
#             delivery_time_in_days=detail.delivery_time_in_days,
#             price=detail.price,
#             features=detail.features,
#             offer_type=detail.offer_type,
#         )
#         serializer = self.serializer_class(order)
#         return Response(serializer.data, status=201)


# class OrderDetailView(RetrieveUpdateDestroyAPIView):
#     """
#     GET /api/orders/{id}/
#     PATCH (status) by business users
#     DELETE by staff only
#     """
#     queryset = Order.objects.all()
#     permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
#     serializer_class = OrderSerializer

#     def get_permissions(self):
#         if self.request.method == 'PATCH':
#             return [IsAuthenticated(), IsBusinessUser()]
#         return super().get_permissions()

#     def get_serializer_class(self):
#         if self.request.method == 'PATCH':
#             return OrderStatusSerializer
#         return OrderSerializer

#     def patch(self, request, *args, **kwargs):
#         """Partial update: only status field."""
#         try:
#             order = self.get_object()
#         except Order.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         self.check_object_permissions(request, order)
#         serializer = self.get_serializer(
#             order, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             full = OrderSerializer(order)
#             return Response(full.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *args, **kwargs):
#         """Delete only for staff users."""
#         try:
#             order = self.get_object()
#         except Order.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         self.check_permissions(request)
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class OrderCountView(APIView):
#     """
#     GET /api/order-count/{business_user_id}/
#     Returns the number of 'in_progress' orders for the specified business user.
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request, business_user_id):
#         # Verify business user exists
#         try:
#             User.objects.get(id=business_user_id)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         # Count open orders
#         count = Order.objects.filter(
#             business_user_id=business_user_id,
#             status='in_progress'
#         ).count()

#         # Serialize and return
#         serializer = OrderCountSerializer({'order_count': count})
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class CompletedOrderCountView(APIView):
#     """
#     GET /api/completed-order-count/{business_user_id}/
#     Returns the number of 'completed' orders for the specified business user.
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request, business_user_id):
#         # Ensure the business user exists
#         try:
#             User.objects.get(id=business_user_id)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         # Count completed orders
#         count = Order.objects.filter(
#             business_user_id=business_user_id,
#             status='completed'
#         ).count()

#         # Serialize and return
#         serializer = CompletedOrderCountSerializer(
#             {'completed_order_count': count})
#         return Response(serializer.data, status=status.HTTP_200_OK)
