# Third-party suppliers
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Local imports
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationTests(APITestCase):
    """
    Tests for user registration endpoint.
    """

    def setUp(self):
        """
        Set up user for registration.
        """
        self.client = APIClient()
        self.url = reverse('registration')
        self.valid_payload = {
            'username': 'exampleUsername',
            'email': 'example@mail.de',
            'password': 'examplePassword',
            'repeated_password': 'examplePassword',
            'type': 'customer',
        }

    def test_registration_success(self):
        """
        Ensure a user registers successfully (HTTP 201).
        """
        response = self.client.post(
            self.url, data=self.valid_payload, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'],
                         self.valid_payload['username'])
        self.assertEqual(response.data['email'], self.valid_payload['email'])
        self.assertIn('user_id', response.data)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, self.valid_payload['username'])
        self.assertEqual(user.email, self.valid_payload['email'])

    def test_registration_missing_fields(self):
        """
        Ensure missing payload returns HTTP 400.
        """
        response = self.client.post(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)

    def test_registration_password_mismatch(self):
        """
        Ensure mismatch passwords return HTTP 400.
        """
        payload = self.valid_payload.copy()
        payload['repeated_password'] = 'wrong'
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
