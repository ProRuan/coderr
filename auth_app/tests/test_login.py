
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase

User = get_user_model()


class LoginTests(APITestCase):
    def setUp(self):
        # Create a user for login tests
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password=make_password('securePassword123'),
            type='customer'
        )
        self.login_url = reverse('login')

    def test_login_success(self):
        """
        Test successful login returns 200 and auth token.
        """
        data = {
            'username': 'testuser',
            'password': 'securePassword123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertEqual(response.data['user_id'], self.user.id)

    def test_login_invalid_credentials(self):
        """
        Test login with wrong credentials returns 400.
        """
        data = {
            'username': 'testuser',
            'password': 'wrongPassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
