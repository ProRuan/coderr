# Third-party suppliers
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Local imports
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class LoginTests(APITestCase):
    """
    Tests for user login endpoint.
    """

    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password=make_password('securePassword123'),
            type='customer'
        )
        self.url = reverse('login')

    def test_login_success(self):
        """
        Ensure valid credentials return HTTP 200 and token.
        """
        data = {
            'username': 'testuser',
            'password': 'securePassword123'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertEqual(response.data['user_id'], self.user.id)

    def test_login_invalid_credentials(self):
        """
        Ensure wrong password returns HTTP 400 with non_field_errors.
        """
        data = {
            'username': 'testuser',
            'password': 'wrong'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
