# Third-party suppliers
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Local imports
from offer_app.models import Offer, OfferDetail

User = get_user_model()


def offers_list_url():
    """
    Get URL of offer list.
    """
    return '/api/offers/'


class OfferListCreateTests(APITestCase):
    """
    Tests for listing and creating offers.
    """

    def setUp(self):
        """
        Set up users and sample offer with 3 details.
        """
        self.client = APIClient()
        self.business = User.objects.create_user(
            username='bizuser',
            email='biz@example.com',
            password='pass',
            type='business',
        )
        self.customer = User.objects.create_user(
            username='custuser',
            email='cust@example.com',
            password='pass',
            type='customer',
        )
        self.offer = Offer.objects.create(
            user=self.business,
            title='Website Design',
            description='Professionelles Website-Design...'
        )
        OfferDetail.objects.bulk_create([
            OfferDetail(
                offer=self.offer, title='Basic', revisions=1,
                delivery_time_in_days=7, price=100,
                features=['A'], offer_type='basic'),
            OfferDetail(
                offer=self.offer, title='Std', revisions=2,
                delivery_time_in_days=5, price=150,
                features=['B'], offer_type='standard'),
            OfferDetail(
                offer=self.offer, title='Pro', revisions=3,
                delivery_time_in_days=3, price=200,
                features=['C'], offer_type='premium'),
        ])

    def test_get_offers_list(self):
        """
        Ensure paginated list of offers can be retrieved (HTTP 200).
        """
        res = self.client.get(offers_list_url(), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)
        offer_data = res.data['results'][0]
        self.assertEqual(offer_data['id'], self.offer.id)
        self.assertEqual(offer_data['min_price'], 100)
        self.assertEqual(offer_data['max_delivery_time'], 7)

    def test_post_offer_unauthenticated(self):
        """
        Ensure unauthenticated users cannot create an offer (HTTP 401).
        """
        res = self.client.post(offers_list_url(), {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_offer_forbidden_non_business(self):
        """
        Ensure customers cannot create offers (HTTP 403).
        """
        self.client.force_authenticate(self.customer)
        res = self.client.post(offers_list_url(), {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_offer_bad_request_too_few_details(self):
        """
        Ensure offer includes 3 details (HTTP 400).
        """
        self.client.force_authenticate(self.business)
        payload = {
            'title': 'Grafikdesign-Paket',
            'description': 'Desc',
            'details': [{
                'title': 'Only', 'revisions': 1,
                'delivery_time_in_days': 1, 'price': 10,
                'features': [], 'offer_type': 'basic'
            }]
        }
        res = self.client.post(offers_list_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('details', res.data)

    def test_post_offer_success(self):
        """
        Ensure valid offer can be created.
        """
        self.client.force_authenticate(self.business)
        payload = {
            'title': 'Grafikdesign-Paket',
            'description': 'Ein umfassendes Grafikdesign-Paket...',
            'details': [
                {
                    'title': 'Basic Design', 'revisions': 2,
                    'delivery_time_in_days': 5, 'price': 100,
                    'features': ['Logo', 'Visitenkarte'],
                    'offer_type': 'basic'
                },
                {
                    'title': 'Standard Design', 'revisions': 5,
                    'delivery_time_in_days': 7, 'price': 200,
                    'features': ['Logo', 'Visitenkarte', 'Briefpapier'],
                    'offer_type': 'standard'
                },
                {
                    'title': 'Premium Design', 'revisions': 10,
                    'delivery_time_in_days': 10, 'price': 500,
                    'features': ['Logo', 'Visitenkarte', 'Briefpapier', 'Flyer'],
                    'offer_type': 'premium'
                }
            ]
        }
        res = self.client.post(offers_list_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], 'Grafikdesign-Paket')
        self.assertEqual(len(res.data['details']), 3)
