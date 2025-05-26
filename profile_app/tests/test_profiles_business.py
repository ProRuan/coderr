# Third-party suppliers
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


def get_business_list_url():
    """
    Get url of business profile list.
    """
    return '/api/profiles/business/'


class BusinessProfileListTests(APITestCase):
    """
    Tests for GET /api/profiles/business/
    """

    def setUp(self):
        self.client = APIClient()
        self.business1 = User.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='buspass',
            type='business',
            first_name='Max',
            last_name='Mustermann'
        )
        User.objects.create_user(
            username='customer1',
            email='cust@example.com',
            password='custpass',
            type='customer'
        )

    def test_list_business_profiles_success(self):
        """
        Ensure authenticated user receives only business profiles (HTTP 200).
        """
        self.client.force_authenticate(self.business1)
        response = self.client.get(get_business_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type'], 'business')

    def test_list_business_profiles_unauthenticated(self):
        """
        Ensure unauthenticated user get denied (HTTP 401).
        """
        response = self.client.get(get_business_list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
