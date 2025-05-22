from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from offer_app.models import Offer, OfferDetail

User = get_user_model()


def offers_list_url():
    return '/api/offers/'


class OfferListCreateTests(APITestCase):
    """
    Tests for GET list and POST create of offers.
    """

    def setUp(self):
        self.client = APIClient()
        # Create users
        self.business = User.objects.create_user(
            username='bizuser', email='biz@example.com', password='pass', type='business'
        )
        self.customer = User.objects.create_user(
            username='custuser', email='cust@example.com', password='pass', type='customer'
        )
        # Create an offer with 3 details for GET list
        self.offer = Offer.objects.create(
            user=self.business,
            title='Website Design',
            description='Professionelles Website-Design...'
        )
        OfferDetail.objects.bulk_create([
            OfferDetail(offer=self.offer, title='Basic', revisions=1,
                        delivery_time_in_days=7, price=100, features=['A'], offer_type='basic'),
            OfferDetail(offer=self.offer, title='Std', revisions=2,
                        delivery_time_in_days=5, price=150, features=['B'], offer_type='standard'),
            OfferDetail(offer=self.offer, title='Pro', revisions=3,
                        delivery_time_in_days=3, price=200, features=['C'], offer_type='premium'),
        ])

    def test_get_offers_list(self):
        response = self.client.get(offers_list_url(), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        # Check pagination keys
        self.assertIn('count', data)
        self.assertIn('results', data)
        # One offer
        self.assertEqual(data['count'], 1)
        offer_data = data['results'][0]
        self.assertEqual(offer_data['id'], self.offer.id)
        self.assertEqual(offer_data['min_price'], 100)
        self.assertEqual(offer_data['min_delivery_time'], 3)
        self.assertEqual(offer_data['user_details']['username'], 'bizuser')

    def test_post_offer_unauthenticated(self):
        payload = {}
        response = self.client.post(offers_list_url(), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_offer_forbidden_non_business(self):
        self.client.force_authenticate(self.customer)
        payload = {}
        response = self.client.post(offers_list_url(), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_offer_bad_request_too_few_details(self):
        self.client.force_authenticate(self.business)
        payload = {
            'title': 'Grafikdesign-Paket',
            'description': 'Desc',
            'details': [
                {'title': 'Only', 'revisions': 1, 'delivery_time_in_days': 1,
                    'price': 10, 'features': [], 'offer_type': 'basic'}
            ]
        }
        response = self.client.post(offers_list_url(), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('details', response.data)

    def test_post_offer_success(self):
        self.client.force_authenticate(self.business)
        payload = {
            'title': 'Grafikdesign-Paket',
            'description': 'Ein umfassendes Grafikdesign-Paket für Unternehmen.',
            'details': [
                {'title': 'Basic Design', 'revisions': 2, 'delivery_time_in_days': 5,
                    'price': 100, 'features': ['Logo', 'Visitenkarte'], 'offer_type': 'basic'},
                {'title': 'Standard Design', 'revisions': 5, 'delivery_time_in_days': 7, 'price': 200,
                    'features': ['Logo', 'Visitenkarte', 'Briefpapier'], 'offer_type': 'standard'},
                {'title': 'Premium Design', 'revisions': 10, 'delivery_time_in_days': 10, 'price': 500,
                    'features': ['Logo', 'Visitenkarte', 'Briefpapier', 'Flyer'], 'offer_type': 'premium'}
            ]
        }
        response = self.client.post(offers_list_url(), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEqual(data['title'], 'Grafikdesign-Paket')
        self.assertEqual(len(data['details']), 3)
        # Verify details were created in DB
        self.assertEqual(Offer.objects.count(), 2)
        new_offer = Offer.objects.get(title='Grafikdesign-Paket')
        self.assertEqual(new_offer.details.count(), 3)
