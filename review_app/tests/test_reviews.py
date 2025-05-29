# Third-party suppliers
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Local imports
from auth_app.models import CustomUser
from review_app.models import Review


class ReviewAPITests(APITestCase):
    """
    Tests for listing and creating reviews.
    """

    def setUp(self):
        """
        Set up sample users and review.
        """
        self.client = APIClient()

        self.customer_user = CustomUser.objects.create_user(
            username='customer1', password='testpass123', type='customer'
        )
        self.business_user = CustomUser.objects.create_user(
            username='business1', password='testpass123', type='business'
        )

        self.review = Review.objects.create(
            reviewer=self.customer_user,
            business_user=self.business_user,
            rating=4,
            description="Sehr professioneller Service."
        )

        self.review_url = reverse('review-list-create')

    def test_get_reviews_authenticated(self):
        """
        Ensure only authenticated user can get reviews (HTTP 200).
        """
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_get_reviews_unauthenticated(self):
        """
        Ensure unauthenticated users cannot get reviews (HTTP 401).
        """
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_success(self):
        """
        Ensure creating an review (HTTP 201).
        """
        new_business = CustomUser.objects.create_user(
            username='business2', password='testpass123', type='business'
        )
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "business_user": new_business.id,
            "rating": 5,
            "description": "Hervorragende Erfahrung!"
        }
        response = self.client.post(self.review_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['business_user'], new_business.id)

    def test_create_review_duplicate(self):
        """
        Ensure user cannot duplicate reviews (HTTP 400).
        """
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "business_user": self.business_user.id,
            "rating": 3,
            "description": "Zweite Bewertung"
        }
        response = self.client.post(self.review_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already created", str(response.data).lower())

    def test_create_review_by_business_user_forbidden(self):
        """
        Ensure business user cannot create review (HTTP 403.)
        """
        self.client.force_authenticate(user=self.business_user)
        data = {
            "business_user": self.customer_user.id,
            "rating": 4,
            "description": "Nicht erlaubt"
        }
        response = self.client.post(self.review_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
