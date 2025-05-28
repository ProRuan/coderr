# Third-party suppliers
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail
from order_app.models import Order


def get_order_list_url():
    """
    Get URL of order list.
    """
    return reverse('order-list-create')


class OrderListCreateTests(APITestCase):
    """
    Tests for listing and updating orders.
    """

    def setUp(self):
        """
        Set up sample users, offers and orders.
        """
        self.client = APIClient()

        self.customer = CustomUser.objects.create_user(
            username='cust', password='pass', type='customer'
        )
        self.business = CustomUser.objects.create_user(
            username='biz', password='pass', type='business'
        )

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
        """
        Ensure retrieving orders related to authenticated user (HTTP 200).
        """
        self.client.force_authenticate(self.customer)
        res = self.client.get(get_order_list_url(), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.order.id)

    def test_get_orders_unauthenticated(self):
        """
        Ensure unauthenticated users cannot get order list (HTTP 401).
        """
        res = self.client.get(get_order_list_url())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_order_success(self):
        """
        Ensure a customer can create order (HTTP 201).
        """
        self.client.force_authenticate(self.customer)
        payload = {'offer_detail_id': self.detail.id}
        res = self.client.post(get_order_list_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.data
        self.assertEqual(data['customer_user'], self.customer.id)
        self.assertEqual(data['business_user'], self.business.id)
        self.assertEqual(data['title'], self.detail.title)

    def test_post_order_missing_offer_detail(self):
        """
        Ensure a request with missing offer detail gets HTTP 400.
        """
        self.client.force_authenticate(self.customer)
        res = self.client.post(get_order_list_url(), {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_order_non_customer(self):
        """
        Ensure business users cannot create orders (HTTP 403).
        """
        self.client.force_authenticate(self.business)
        payload = {'offer_detail_id': self.detail.id}
        res = self.client.post(get_order_list_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_order_not_found(self):
        """
        Ensure providing an invalid offer detail id gets HTTP 404.
        """
        self.client.force_authenticate(self.customer)
        payload = {'offer_detail_id': 9999}
        res = self.client.post(get_order_list_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
