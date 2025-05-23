# review/tests/test_reviews.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from auth_app.models import CustomUser
from review_app.models import Review


class ReviewAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a customer and business user
        self.customer_user = CustomUser.objects.create_user(
            username='customer1', password='testpass123', type='customer'
        )
        self.business_user = CustomUser.objects.create_user(
            username='business1', password='testpass123', type='business'
        )

        # URL for review list/create
        self.review_url = reverse('review-list-create')

    def test_get_reviews_authenticated(self):
        # Create a review
        Review.objects.create(
            reviewer=self.customer_user,
            business_user=self.business_user,
            rating=4,
            description="Sehr professioneller Service."
        )

        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.review_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_get_reviews_unauthenticated(self):
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_success(self):
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Hervorragende Erfahrung!"
        }
        response = self.client.post(self.review_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['business_user'], self.business_user.id)

    def test_create_review_duplicate(self):
        Review.objects.create(
            reviewer=self.customer_user,
            business_user=self.business_user,
            rating=4,
            description="Erste Bewertung"
        )

        self.client.force_authenticate(user=self.customer_user)
        data = {
            "business_user": self.business_user.id,
            "rating": 3,
            "description": "Zweite Bewertung"
        }
        response = self.client.post(self.review_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already reviewed", str(response.data).lower())

    def test_create_review_by_business_user_forbidden(self):
        self.client.force_authenticate(user=self.business_user)
        data = {
            "business_user": self.customer_user.id,
            "rating": 4,
            "description": "Nicht erlaubt"
        }
        response = self.client.post(self.review_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
