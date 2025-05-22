# base_info/tests/test_base_info.py
# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# 3. Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer
from review_app.models import Review


class BaseInfoTests(APITestCase):
    """
    Tests for GET /api/base-info/ endpoint returning platform statistics.
    """

    def setUp(self):
        # Create business users and customer users
        biz1 = CustomUser.objects.create_user(
            username='biz1', password='pass', type='business')
        biz2 = CustomUser.objects.create_user(
            username='biz2', password='pass', type='business')
        cust1 = CustomUser.objects.create_user(
            username='cust1', password='pass', type='customer')
        cust2 = CustomUser.objects.create_user(
            username='cust2', password='pass', type='customer')
        # Create offers
        Offer.objects.create(user=biz1, title='Off1', description='D1')
        Offer.objects.create(user=biz1, title='Off2', description='D2')
        Offer.objects.create(user=biz2, title='Off3', description='D3')
        # Create reviews (use distinct reviewer for biz1)
        Review.objects.create(business_user=biz1,
                              reviewer=cust1, rating=5, description='Great')
        Review.objects.create(business_user=biz1,
                              reviewer=cust2, rating=4, description='Good')
        # Review for biz2
        Review.objects.create(business_user=biz2,
                              reviewer=cust1, rating=3, description='Okay')

    def test_get_base_info_success(self):
        """
        Ensure GET returns correct counts and average rating.
        """
        url = reverse('base-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        # Total reviews: 3
        self.assertEqual(data['valuation_count'], 3)
        # Average rating: (5+4+3)/3 = 4.0
        self.assertEqual(data['average_rating'], 4.0)
        # Business user count: 2
        self.assertEqual(data['business_user_count'], 2)
        # Offer count: 3
        self.assertEqual(data['offer_count'], 3)

    def test_get_base_info_zero(self):
        """
        When no data, endpoint returns zeros and 0.0.
        """
        # Clear all
        Review.objects.all().delete()
        Offer.objects.all().delete()
        CustomUser.objects.all().delete()

        url = reverse('base-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['valuation_count'], 0)
        self.assertEqual(data['average_rating'], 0.0)
        self.assertEqual(data['business_user_count'], 0)
        self.assertEqual(data['offer_count'], 0)
