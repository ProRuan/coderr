# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class AccountTests(APITestCase):
#     def test_registration(self):
#         """
#         Ensure we can create a new account.
#         """
#         url = reverse('registration')
#         data = {
#             'username': 'marioSuper',
#             'email': 'super@mail.com',
#             'password': 'Test123!',
#             'repeated_password': 'Test123!',
#             'type': 'customer'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(User.objects.get().username, 'marioSuper')


from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationTests(TestCase):
    """
    Tests for user registration endpoint using DRF APIClient.
    """

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('registration')
        self.valid_payload = {
            'username': 'exampleUsername',
            'email': 'example@mail.de',
            'password': 'examplePassword',
            'repeated_password': 'examplePassword',
            'type': 'customer',
        }

    def test_user_registration_success(self):
        """
        Ensure a new user can register successfully (HTTP 201).
        """
        response = self.client.post(
            self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check response body contains expected fields
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'],
                         self.valid_payload['username'])
        self.assertEqual(response.data['email'], self.valid_payload['email'])
        self.assertIn('user_id', response.data)
        # Ensure user was created in database
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, self.valid_payload['username'])
        self.assertEqual(user.email, self.valid_payload['email'])

    def test_user_registration_bad_request_missing_fields(self):
        """
        Registration without payload should return HTTP 400.
        """
        response = self.client.post(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Expect errors for required fields
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)

    def test_user_registration_bad_request_password_mismatch(self):
        """
        Registration with mismatched passwords should return HTTP 400.
        """
        payload = self.valid_payload.copy()
        payload['repeated_password'] = 'wrongPassword'
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Expect validation error on password field
        self.assertIn('password', response.data)
