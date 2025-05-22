from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


def customer_list_url():
    return '/api/profile/customer/'


class CustomerProfileListTests(APITestCase):
    """
    Tests for CustomerProfileListView GET endpoint.
    """

    def setUp(self):
        self.client = APIClient()
        # Create a customer user
        self.customer1 = User.objects.create_user(
            username='customer_jane',
            email='jane@customer.de',
            password='custpass',
            type='customer',
            first_name='Jane',
            last_name='Doe'
        )
        # Create a business user (should not appear)
        User.objects.create_user(
            username='business_user',
            email='biz@business.de',
            password='bizpass',
            type='business',
            first_name='Biz',
            last_name='Owner'
        )
        # Set uploaded_at for customer
        self.customer1.uploaded_at = timezone.make_aware(
            timezone.datetime(2023, 9, 15, 9, 0, 0))
        self.customer1.save()

    def test_list_customer_profiles_success(self):
        self.client.force_authenticate(self.customer1)
        url = customer_list_url()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)
        profile = data[0]
        self.assertEqual(profile['id'], self.customer1.pk)
        self.assertEqual(profile['username'], 'customer_jane')
        self.assertEqual(profile['type'], 'customer')
        self.assertEqual(profile['uploaded_at'], '2023-09-15T09:00:00Z')

    def test_list_customer_profiles_unauthenticated(self):
        url = customer_list_url()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
