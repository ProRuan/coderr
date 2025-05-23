# order/tests/test_orders_detail.py
# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# 3. Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail
from order_app.models import Order


def detail_url(pk):
    return reverse('order-detail', args=[pk])


class OrderDetailTests(APITestCase):
    """
    Tests for GET, PATCH, and DELETE on /api/orders/{id}/
    """

    def setUp(self):
        self.client = APIClient()
        # Users
        self.customer = CustomUser.objects.create_user(
            username='cust', password='pass', type='customer'
        )
        self.business = CustomUser.objects.create_user(
            username='biz', password='pass', type='business'
        )
        self.admin = CustomUser.objects.create_user(
            username='admin', password='pass', type='business', is_staff=True
        )
        # Offer and detail
        offer = Offer.objects.create(
            user=self.business, title='Logo Design', description='D')
        self.detail = OfferDetail.objects.create(
            offer=offer,
            title='Logo Design',
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=['Logo Design', 'Visitenkarten'],
            offer_type='basic'
        )
        # Create an order
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
        """Authenticated user can GET order detail."""
        self.client.force_authenticate(self.customer)
        res = self.client.get(detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertEqual(data['id'], self.order.id)
        self.assertEqual(data['status'], 'in_progress')

    def test_get_order_unauthenticated(self):
        """Unauthenticated GET returns 401."""
        res = self.client.get(detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_not_found(self):
        """GET non-existent order returns 404."""
        self.client.force_authenticate(self.customer)
        res = self.client.get(detail_url(9999))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_order_success(self):
        """Business user can PATCH status."""
        self.client.force_authenticate(self.business)
        payload = {'status': 'completed'}
        res = self.client.patch(detail_url(
            self.order.id), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'completed')

    def test_patch_order_invalid_status(self):
        """PATCH invalid status returns 400."""
        self.client.force_authenticate(self.business)
        res = self.client.patch(detail_url(self.order.id), {
                                'status': 'invalid'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_unauthenticated(self):
        """Unauthenticated PATCH returns 401."""
        res = self.client.patch(detail_url(self.order.id), {
                                'status': 'completed'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_order_forbidden(self):
        """Customer user cannot PATCH: returns 403."""
        self.client.force_authenticate(self.customer)
        res = self.client.patch(detail_url(self.order.id), {
                                'status': 'completed'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_not_found(self):
        """PATCH non-existent order returns 404."""
        self.client.force_authenticate(self.business)
        res = self.client.patch(detail_url(
            9999), {'status': 'completed'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_success(self):
        """Admin user can DELETE order."""
        self.client.force_authenticate(self.admin)
        res = self.client.delete(detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_delete_order_unauthenticated(self):
        """Unauthenticated DELETE returns 401."""
        res = self.client.delete(detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_order_forbidden(self):
        """Non-admin DELETE returns 403."""
        self.client.force_authenticate(self.business)
        res = self.client.delete(detail_url(self.order.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_not_found(self):
        """DELETE non-existent order returns 404."""
        self.client.force_authenticate(self.admin)
        res = self.client.delete(detail_url(9999))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
