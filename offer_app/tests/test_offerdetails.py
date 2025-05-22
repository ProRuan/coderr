# offer/tests/test_offerdetails.py
# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# 3. Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail


def detail_url(pk):
    return f'/api/offerdetails/{pk}/'


class OfferDetailRetrieveTests(APITestCase):
    """
    Tests for retrieving a single OfferDetail via OfferDetailRetrieveAPIView.
    """

    def setUp(self):
        # Create business user and authenticate
        self.user = CustomUser.objects.create_user(
            username='biz', password='pass', type='business'
        )
        self.client = APIClient()
        # Create an offer and a detail
        self.offer = Offer.objects.create(
            user=self.user,
            title='Test Offer', description='Desc'
        )
        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title='Basic Design',
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=['Logo Design', 'Visitenkarte'],
            offer_type='basic'
        )

    def test_get_offerdetail_success(self):
        """
        Authenticated user can retrieve offer detail (200).
        """
        self.client.force_authenticate(self.user)
        url = detail_url(self.detail.id)
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertEqual(data['id'], self.detail.id)
        self.assertEqual(data['title'], 'Basic Design')
        self.assertEqual(data['revisions'], 2)
        self.assertEqual(data['delivery_time_in_days'], 5)
        # DRF returns Decimal as string
        self.assertEqual(data['price'], '100.00')
        self.assertEqual(data['features'], ['Logo Design', 'Visitenkarte'])
        self.assertEqual(data['offer_type'], 'basic')

    def test_get_offerdetail_unauthenticated(self):
        """
        Unauthenticated access returns 401.
        """
        url = detail_url(self.detail.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offerdetail_not_found(self):
        """
        Requesting nonexistent detail returns 404.
        """
        self.client.force_authenticate(self.user)
        url = detail_url(9999)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
