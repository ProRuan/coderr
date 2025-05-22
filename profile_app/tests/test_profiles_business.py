from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


def business_list_url():
    return '/api/profile/business/'


class BusinessProfileListTests(APITestCase):
    """
    Tests for BusinessProfileListView GET endpoint.
    """

    def setUp(self):
        self.client = APIClient()
        # Create a business user
        self.business1 = User.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='buspass',
            type='business',
            first_name='Max',
            last_name='Mustermann'
        )
        # Create a customer user (should not appear)
        User.objects.create_user(
            username='customer1',
            email='cust@example.com',
            password='custpass',
            type='customer',
            first_name='Cust',
            last_name='User'
        )

    def test_list_business_profiles_success(self):
        self.client.force_authenticate(self.business1)
        url = business_list_url()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        # Only business profiles should be in the list
        self.assertEqual(len(data), 1)
        profile = data[0]
        self.assertEqual(profile['id'], self.business1.pk)
        self.assertEqual(profile['username'], 'max_business')
        self.assertEqual(profile['type'], 'business')

    def test_list_business_profiles_unauthenticated(self):
        url = business_list_url()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
