# Third-party suppliers
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail
from order_app.models import Order


def get_order_detail_url(pk):
    """
    Get URL of order detail.
    """
    return reverse('order-detail', args=[pk])


class OrderDetailTests(APITestCase):
    """
    Tests for retrieving, updating and deleting orders.
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
        self.admin = CustomUser.objects.create_user(
            username='admin', password='pass', type='business', is_staff=True
        )

        offer = Offer.objects.create(
            user=self.business,
            title='Logo Design',
            description='D'
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

    def test_get_order_success(self):
        """
        Ensure authenticated user can retrieve order (HTTP 200).
        """
        self.client.force_authenticate(self.customer)
        res = self.client.get(get_order_detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertEqual(data['id'], self.order.id)
        self.assertEqual(data['status'], 'in_progress')

    def test_get_order_unauthenticated(self):
        """
        Ensure unauthenticated user cannot GET order (HTTP 401).
        """
        res = self.client.get(get_order_detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_not_found(self):
        """
        Ensure non-existend order returns HTTP 404.
        """
        self.client.force_authenticate(self.customer)
        res = self.client.get(get_order_detail_url(9999))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_order_success(self):
        """
        Ensure business user can update order status (HTTP 200).
        """
        self.client.force_authenticate(self.business)
        payload = {'status': 'completed'}
        res = self.client.patch(get_order_detail_url(
            self.order.id), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'completed')

    def test_patch_order_invalid_status(self):
        """
        Ensure updating order with invalid status gets HTTP 404.
        """
        self.client.force_authenticate(self.business)
        res = self.client.patch(get_order_detail_url(self.order.id), {
                                'status': 'invalid'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_unauthenticated(self):
        """
        Ensure unauthenticated user cannot update order (HTTP 401).
        """
        res = self.client.patch(get_order_detail_url(self.order.id), {
                                'status': 'completed'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_order_forbidden(self):
        """
        Ensure customer cannot update order status (HTTP 403).
        """
        self.client.force_authenticate(self.customer)
        res = self.client.patch(get_order_detail_url(self.order.id), {
                                'status': 'completed'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_not_found(self):
        """
        Ensure updating non-existent order returns HTTP 404.
        """
        self.client.force_authenticate(self.business)
        res = self.client.patch(get_order_detail_url(
            9999), {'status': 'completed'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_success(self):
        """
        Ensure admin user can delete order (HTTP 204).
        """
        self.client.force_authenticate(self.admin)
        res = self.client.delete(get_order_detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_delete_order_unauthenticated(self):
        """
        Ensure unauthenticated user cannot delete order (HTTP 401).
        """
        res = self.client.delete(get_order_detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_order_forbidden(self):
        """
        Ensure non-admin cannot delete order (HTTP 403).
        """
        self.client.force_authenticate(self.business)
        res = self.client.delete(get_order_detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_not_found(self):
        """
        Ensure deleting non-existent order returns HTTP 404.
        """
        self.client.force_authenticate(self.admin)
        res = self.client.delete(get_order_detail_url(9999))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
