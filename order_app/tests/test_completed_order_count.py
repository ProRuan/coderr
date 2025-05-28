# Third-party suppliers
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail
from order_app.models import Order


def get_completed_order_count_url(business_id):
    """
    Get URL of completed order count.
    """
    return reverse('completed-order-count', args=[business_id])


class CompletedOrderCountTests(APITestCase):
    """
    Tests for retrieving the amount of 'completed' orders.
    """

    def setUp(self):
        """
        Set up sample users, offers and orders.
        """
        self.client = APIClient()

        self.business = CustomUser.objects.create_user(
            username='biz', password='pass', type='business'
        )
        self.other_business = CustomUser.objects.create_user(
            username='biz2', password='pass', type='business'
        )
        self.customer = CustomUser.objects.create_user(
            username='cust', password='pass', type='customer'
        )

        offer = Offer.objects.create(
            user=self.business, title='Off', description='D'
        )
        detail = OfferDetail.objects.create(
            offer=offer,
            title='Detail', revisions=1,
            delivery_time_in_days=1, price=50,
            features=['X'], offer_type='basic'
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
        Order.objects.create(
            customer_user=self.customer,
            business_user=self.other_business,
            title=detail.title, revisions=detail.revisions,
            delivery_time_in_days=1, price=detail.price,
            features=detail.features, offer_type=detail.offer_type,
            status='completed'
        )

    def test_get_completed_order_count_success(self):
        """
        Ensure authenticated user gets amount of completed order (HTTP 200).
        """
        self.client.force_authenticate(self.customer)
        url = get_completed_order_count_url(self.business.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['completed_order_count'], 2)

    def test_get_completed_order_count_unauthenticated(self):
        """
        Ensure unauthenticated request returns HTTP 401.
        """
        url = get_completed_order_count_url(self.business.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_completed_order_count_business_not_found(self):
        """
        Ensure non-existent business user returns HTTP 404.
        """
        self.client.force_authenticate(self.customer)
        url = get_completed_order_count_url(9999)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
