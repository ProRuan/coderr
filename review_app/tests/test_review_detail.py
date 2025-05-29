# Third-party suppliers
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Local imports
from auth_app.models import CustomUser
from review_app.models import Review


class ReviewDetailAPITests(APITestCase):
    """
    Tests for updating and deleting a review.
    """

    def setUp(self):
        """
        Set up sample users and a review.
        """
        self.client = APIClient()

        self.customer = CustomUser.objects.create_user(
            username='customer', password='testpass123', type='customer'
        )
        self.business = CustomUser.objects.create_user(
            username='business', password='testpass123', type='business'
        )
        self.other_user = CustomUser.objects.create_user(
            username='other', password='testpass123', type='customer'
        )

        self.review = Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=4,
            description="Guter Service"
        )
        self.review_url = reverse('review-detail', args=[self.review.id])

    def test_get_review_authenticated(self):
        """
        Ensure authenticated user can retrieve a review (HTTP 200).
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.review.id)
        self.assertEqual(response.data['rating'], 4)

    def test_get_review_unauthenticated(self):
        """
        Ensure unauthenticated users cannot retrieve a review (HTTP 401).
        """
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_review_by_reviewer_success(self):
        """
        Ensure reviewer can update their own review (HTTP 200).
        """
        self.client.force_authenticate(user=self.customer)
        data = {
            "rating": 5,
            "description": "Noch besser als erwartet!"
        }
        response = self.client.patch(self.review_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)
        self.assertIn("Noch besser", response.data["description"])

    def test_patch_review_by_other_user_forbidden(self):
        """
        Ensure other users cannot update another user's review (HTTP 403).
        """
        self.client.force_authenticate(user=self.other_user)
        data = {"rating": 3, "description": "Nicht erlaubt"}
        response = self.client.patch(self.review_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_review_invalid_rating(self):
        """
        Ensure invalid rating value returns error (HTTP 400).
        """
        self.client.force_authenticate(user=self.customer)
        data = {"rating": 10, "description": "Ungültig"}
        response = self.client.patch(self.review_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("rating", response.data)

    def test_patch_review_unauthenticated(self):
        """
        Ensure unauthenticated users cannot update a review (HTTP 401).
        """
        data = {"rating": 2, "description": "Nicht erlaubt"}
        response = self.client.patch(self.review_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_review_by_reviewer_success(self):
        """
        Ensure reviewer can delete their own review (HTTP 204).
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.delete(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_delete_review_by_other_user_forbidden(self):
        """
        Ensure other users cannot delete another user's review (HTTP 403).
        """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_unauthenticated(self):
        """
        Ensure unauthenticated users cannot delete a review (HTTP 401).
        """
        response = self.client.delete(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
