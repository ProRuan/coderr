# Third-party suppliers
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


# Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail


def detail_url(pk):
    """
    Get URL of an offer detail.
    """
    return f'/api/offerdetails/{pk}/'


class OfferDetailRetrieveTests(APITestCase):
    """
    Tests for retrieving an offer detail.
    """

    def setUp(self):
        """
        Set up user and offer detail.
        """
        self.user = CustomUser.objects.create_user(
            username='biz', password='pass', type='business'
        )
        self.client = APIClient()
        self.offer = Offer.objects.create(
            user=self.user, title='Test Offer', description='Desc'
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
        Ensure authenticated user can retrieve offer detail (HTTP 200).
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
        self.assertEqual(data['price'], 100)
        self.assertEqual(data['features'], ['Logo Design', 'Visitenkarte'])
        self.assertEqual(data['offer_type'], 'basic')

    def test_get_offerdetail_unauthenticated(self):
        """
        Ensure unauthenticated users cannot retrieve offer detail (HTTP 401).
        """
        url = detail_url(self.detail.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offerdetail_not_found(self):
        """
        Ensure HTTP 404 is returned when offer detail is not found.
        """
        self.client.force_authenticate(self.user)
        url = detail_url(9999)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
