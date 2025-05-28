# Third-party suppliers
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


def get_customer_list_url():
    """
    Get url of customer profile list.
    """
    return '/api/profiles/customer/'


class CustomerProfileListTests(APITestCase):
    """
    Tests for GET /api/profiles/customer/
    """

    def setUp(self):
        """
        Set up users and sample profiles.
        """
        self.client = APIClient()
        self.customer1 = User.objects.create_user(
            username='customer_jane',
            email='jane@customer.de',
            password='custpass',
            type='customer',
            first_name='Jane',
            last_name='Doe'
        )
        self.customer1.uploaded_at = timezone.make_aware(
            timezone.datetime(2023, 9, 15, 9, 0, 0)
        )
        self.customer1.save()

        User.objects.create_user(
            username='business_user',
            email='biz@business.de',
            password='bizpass',
            type='business'
        )

    def test_list_customer_profiles_success(self):
        """
        Ensure authenticated user receives only customer profiles (HTTP 200).
        """
        self.client.force_authenticate(self.customer1)
        response = self.client.get(get_customer_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type'], 'customer')

    def test_list_customer_profiles_unauthenticated(self):
        """
        Ensure unauthenticated user get denied (HTTP 401).
        """
        response = self.client.get(get_customer_list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
