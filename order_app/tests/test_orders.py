# order/tests/test_orders.py
# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone

# 3. Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail
from order_app.models import Order


def orders_url():
    return reverse('order-list-create')


class OrderListCreateTests(APITestCase):
    """
    Tests for GET and POST /api/orders/ endpoint.
    """

    def setUp(self):
        self.client = APIClient()
        # Create users
        self.customer = CustomUser.objects.create_user(
            username='cust', password='pass', type='customer'
        )
        self.business = CustomUser.objects.create_user(
            username='biz', password='pass', type='business'
        )
        # Create an offer and an offer detail
        offer = Offer.objects.create(
            user=self.business,
            title='Logo Design',
            description='Desc'
        )
        self.detail = OfferDetail.objects.create(
            offer=offer,
            title='Logo Design',
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=['Logo Design', 'Visitenkarten'],
            offer_type='basic'
        )
        # Create an existing order
        self.order = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title=self.detail.title,
            revisions=self.detail.revisions,
            delivery_time_in_days=self.detail.delivery_time_in_days,
            price=self.detail.price,
            features=self.detail.features,
            offer_type=self.detail.offer_type,
            status='in_progress'
        )

    def test_get_orders_authenticated(self):
        """GET returns orders related to authenticated user."""
        self.client.force_authenticate(self.customer)
        res = self.client.get(orders_url(), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertIsInstance(data, list)
        # customer sees their order
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.order.id)

    def test_get_orders_unauthenticated(self):
        """GET without auth returns 401."""
        res = self.client.get(orders_url())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_order_success(self):
        """Customer can create order from valid offer_detail_id."""
        self.client.force_authenticate(self.customer)
        payload = {'offer_detail_id': self.detail.id}
        res = self.client.post(orders_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.data
        self.assertEqual(data['customer_user'], self.customer.id)
        self.assertEqual(data['business_user'], self.business.id)
        self.assertEqual(data['title'], self.detail.title)

    def test_post_order_missing_offer_detail(self):
        """Missing offer_detail_id returns 403."""
        self.client.force_authenticate(self.customer)
        res = self.client.post(orders_url(), {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_order_non_customer(self):
        """Business user cannot create order: returns 403."""
        self.client.force_authenticate(self.business)
        payload = {'offer_detail_id': self.detail.id}
        res = self.client.post(orders_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_order_not_found(self):
        """Invalid offer_detail_id returns 404."""
        self.client.force_authenticate(self.customer)
        payload = {'offer_detail_id': 9999}
        res = self.client.post(orders_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
