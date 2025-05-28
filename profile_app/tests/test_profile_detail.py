# Third-party suppliers
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class ProfileDetailTests(APITestCase):
    """
    Tests for GET and PATCH on /api/profile/{pk}/.
    """

    def setUp(self):
        """
        Set up users and sample profiles.
        """
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username='max_mustermann',
            email='max@business.de',
            password='ownerpass',
            type='business',
            first_name='Max',
            last_name='Mustermann',
        )
        self.owner.file = 'profile_picture.jpg'
        self.owner.location = 'Berlin'
        self.owner.tel = '123456789'
        self.owner.description = 'Business description'
        self.owner.working_hours = '9-17'
        self.owner.created_at = timezone.make_aware(
            timezone.datetime(2023, 1, 1, 12, 0, 0)
        )
        self.owner.save()

        self.other = User.objects.create_user(
            username='other_user',
            email='other@example.com',
            password='otherpass',
            type='business',
            first_name='Other',
            last_name='User',
        )

    def profile_url(self, pk):
        """
        Get profile detail url.
        """
        return f'/api/profile/{pk}/'

    def test_get_profile_success(self):
        """
        Ensure authenticated user gets profile successfully (HTTP 200).
        """
        self.client.force_authenticate(self.owner)
        response = self.client.get(self.profile_url(self.owner.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.owner.username)

    def test_get_profile_unauthenticated(self):
        """
        Ensure unauthenticated user get HTTP 401.
        """
        response = self.client.get(self.profile_url(self.owner.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_not_found(self):
        """
        Ensure authenticated user gets HTTP 404 for non-existing profile.
        """
        self.client.force_authenticate(self.owner)
        response = self.client.get(self.profile_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_profile_success(self):
        """
        Ensure profile owner can patch profile successfully (HTTP 200).
        """
        self.client.force_authenticate(self.owner)
        payload = {
            'tel': '987654321',
            'description': 'Updated business description',
            'email': 'new_email@business.de'
        }
        response = self.client.patch(
            self.profile_url(self.owner.pk), data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tel'], payload['tel'])

    def test_patch_profile_unauthenticated(self):
        """
        Ensure unauthenticated user gets HTTP 401 on PATCH.
        """
        response = self.client.patch(self.profile_url(self.owner.pk), data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_forbidden(self):
        """
        Ensure authenticated user gets HTTP 403 PATCHing others´ profiles.
        """
        self.client.force_authenticate(self.other)
        response = self.client.patch(self.profile_url(
            self.owner.pk), data={'location': 'Hamburg'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_not_found(self):
        """
        Ensure authenticated user gets HTTP 404 PATCHing non-existing profile.
        """
        self.client.force_authenticate(self.owner)
        response = self.client.patch(self.profile_url(9999), data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
