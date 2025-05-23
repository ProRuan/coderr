# order/tests/test_completed_order_count.py
# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# 3. Local imports
from auth_app.models import CustomUser
from order_app.models import Order
from offer_app.models import Offer, OfferDetail


def completed_order_count_url(business_id):
    return f'/api/completed-order-count/{business_id}/'


class CompletedOrderCountTests(APITestCase):
    """
    Tests for GET /api/completed-order-count/{business_user_id}/ endpoint.
    """

    def setUp(self):
        self.client = APIClient()
        # Create business users and a customer
        self.business = CustomUser.objects.create_user(
            username='biz', password='pass', type='business'
        )
        self.other_business = CustomUser.objects.create_user(
            username='biz2', password='pass', type='business'
        )
        self.customer = CustomUser.objects.create_user(
            username='cust', password='pass', type='customer'
        )
        # Create an offer and its detail
        offer = Offer.objects.create(
            user=self.business, title='Off', description='D'
        )
        detail = OfferDetail.objects.create(
            offer=offer,
            title='Detail', revisions=1,
            delivery_time_in_days=1, price=50,
            features=['X'], offer_type='basic'
        )
        # Orders for self.business: 2 completed, 1 in_progress
        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title=detail.title, revisions=detail.revisions,
            delivery_time_in_days=1, price=detail.price,
            features=detail.features, offer_type=detail.offer_type,
            status='completed'
        )
        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title=detail.title, revisions=detail.revisions,
            delivery_time_in_days=1, price=detail.price,
            features=detail.features, offer_type=detail.offer_type,
            status='completed'
        )
        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title=detail.title, revisions=detail.revisions,
            delivery_time_in_days=1, price=detail.price,
            features=detail.features, offer_type=detail.offer_type,
            status='in_progress'
        )
        # Completed order for other business (should be ignored)
        Order.objects.create(
            customer_user=self.customer,
            business_user=self.other_business,
            title=detail.title, revisions=detail.revisions,
            delivery_time_in_days=1, price=detail.price,
            features=detail.features, offer_type=detail.offer_type,
            status='completed'
        )

    def test_get_completed_order_count_success(self):
        """Authenticated user gets correct completed order count."""
        self.client.force_authenticate(self.customer)
        url = completed_order_count_url(self.business.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['completed_order_count'], 2)

    def test_get_completed_order_count_unauthenticated(self):
        """Unauthenticated request returns 401."""
        url = completed_order_count_url(self.business.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_completed_order_count_business_not_found(self):
        """Non-existent business user returns 404."""
        self.client.force_authenticate(self.customer)
        url = completed_order_count_url(9999)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
