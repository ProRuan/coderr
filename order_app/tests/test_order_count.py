# order/tests/test_order_count.py
# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# 3. Local imports
from auth_app.models import CustomUser
from order_app.models import Order
from offer_app.models import Offer, OfferDetail


def open_order_count_url(business_id):
    return f'/api/order-count/{business_id}/'


class OpenOrderCountTests(APITestCase):
    """
    Tests for GET /api/order-count/{business_user_id}/ endpoint.
    """

    def setUp(self):
        # Create users
        self.business = CustomUser.objects.create_user(
            username='biz', password='pass', type='business'
        )
        self.other_business = CustomUser.objects.create_user(
            username='biz2', password='pass', type='business'
        )
        self.customer = CustomUser.objects.create_user(
            username='cust', password='pass', type='customer'
        )
        # Create offers and details for business
        offer = Offer.objects.create(
            user=self.business, title='Off', description='D')
        detail = OfferDetail.objects.create(
            offer=offer,
            title='Detail', revisions=1,
            delivery_time_in_days=1, price=50,
            features=['X'], offer_type='basic'
        )
        # Create orders in various statuses
        Order.objects.create(
            customer_user=self.customer, business_user=self.business,
            title=detail.title, revisions=detail.revisions,
            delivery_time_in_days=1, price=detail.price,
            features=detail.features, offer_type=detail.offer_type,
            status='in_progress'
        )
        Order.objects.create(
            customer_user=self.customer, business_user=self.business,
            title=detail.title, revisions=detail.revisions,
            delivery_time_in_days=1, price=detail.price,
            features=detail.features, offer_type=detail.offer_type,
            status='completed'
        )
        # Another in_progress for other business
        Order.objects.create(
            customer_user=self.customer, business_user=self.other_business,
            title=detail.title, revisions=detail.revisions,
            delivery_time_in_days=1, price=detail.price,
            features=detail.features, offer_type=detail.offer_type,
            status='in_progress'
        )

    def test_get_open_order_count_success(self):
        """
        Authenticated user gets correct count of in_progress orders.
        """
        self.client.force_authenticate(self.customer)
        url = open_order_count_url(self.business.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['order_count'], 1)

    def test_get_open_order_count_unauthenticated(self):
        """
        Unauthenticated request returns 401.
        """
        url = open_order_count_url(self.business.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_open_order_count_business_not_found(self):
        """
        Non-existent business user returns 404.
        """
        self.client.force_authenticate(self.customer)
        url = open_order_count_url(9999)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
