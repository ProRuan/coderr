from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ProfileDetailTests(APITestCase):
    """
    Tests for ProfileDetailAPIView GET and PATCH endpoints.
    """

    def setUp(self):
        self.client = APIClient()
        # Create a business user as profile owner
        self.owner = User.objects.create_user(
            username='max_mustermann',
            email='max@business.de',
            password='ownerpass',
            type='business',
            first_name='Max',
            last_name='Mustermann'
        )
        # Populate additional profile fields
        self.owner.file = 'profile_picture.jpg'
        self.owner.location = 'Berlin'
        self.owner.tel = '123456789'
        self.owner.description = 'Business description'
        self.owner.working_hours = '9-17'
        # Set a known created_at for testing
        self.owner.created_at = timezone.make_aware(
            timezone.datetime(2023, 1, 1, 12, 0, 0))
        self.owner.save()

        # Other user for forbidden tests
        self.other = User.objects.create_user(
            username='other_user',
            email='other@example.com',
            password='otherpass',
            type='business',
            first_name='Other',
            last_name='User'
        )

    def profile_url(self, pk):
        return f'/api/profile/{pk}/'

    # GET /api/profile/{pk}/
    def test_get_profile_success(self):
        self.client.force_authenticate(self.owner)
        url = self.profile_url(self.owner.pk)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        # Assert returned fields
        self.assertEqual(data['id'], self.owner.pk)
        self.assertEqual(data['username'], 'max_mustermann')
        self.assertEqual(data['email'], 'max@business.de')
        self.assertEqual(data['location'], 'Berlin')
        self.assertEqual(data['type'], 'business')

    def test_get_profile_unauthenticated(self):
        url = self.profile_url(self.owner.pk)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_not_found(self):
        self.client.force_authenticate(self.owner)
        url = self.profile_url(9999)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # PATCH /api/profile/{pk}/
    def test_patch_profile_success(self):
        self.client.force_authenticate(self.owner)
        url = self.profile_url(self.owner.pk)
        payload = {
            'first_name': 'Max',
            'last_name': 'Mustermann',
            'location': 'Berlin',
            'tel': '987654321',
            'description': 'Updated business description',
            'working_hours': '10-18',
            'email': 'new_email@business.de'
        }
        response = self.client.patch(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        # Assert updates reflected
        self.assertEqual(data['tel'], '987654321')
        self.assertEqual(data['description'], 'Updated business description')
        self.assertEqual(data['email'], 'new_email@business.de')

    def test_patch_profile_unauthenticated(self):
        url = self.profile_url(self.owner.pk)
        response = self.client.patch(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_forbidden(self):
        self.client.force_authenticate(self.other)
        url = self.profile_url(self.owner.pk)
        response = self.client.patch(
            url, data={'location': 'Hamburg'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_not_found(self):
        self.client.force_authenticate(self.owner)
        url = self.profile_url(9999)
        response = self.client.patch(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
