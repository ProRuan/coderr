from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from offer_app.models import Offer, OfferDetail

User = get_user_model()


def offer_detail_url(pk):
    return f'/api/offers/{pk}/'


class OfferDetailTests(APITestCase):
    """
    Tests for GET, PATCH, DELETE on OfferDetailView.
    """

    def setUp(self):
        self.client = APIClient()
        # Create users
        self.owner = User.objects.create_user(
            username='owner', email='owner@example.com', password='pass', type='business'
        )
        self.other = User.objects.create_user(
            username='other', email='other@example.com', password='pass', type='business'
        )
        # Create an offer with 3 details
        self.offer = Offer.objects.create(
            user=self.owner,
            title='Grafikdesign-Paket',
            description='Ein umfassendes Grafikdesign-Paket für Unternehmen.'
        )
        self.details = []
        for idx, title in enumerate(['Basic', 'Standard', 'Premium'], start=1):
            detail = OfferDetail.objects.create(
                offer=self.offer,
                title=f'{title} Design',
                revisions=idx * 2,
                delivery_time_in_days=idx * 5,
                price=idx * 50,
                features=['X', 'Y'],
                offer_type=title.lower()
            )
            self.details.append(detail)

    def test_get_offer_success(self):
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(self.offer.pk)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['id'], self.offer.pk)
        self.assertEqual(data['title'], 'Grafikdesign-Paket')
        self.assertEqual(len(data['details']), 3)
        # min_price and min_delivery_time
        self.assertEqual(data['min_price'], 50)
        self.assertEqual(data['min_delivery_time'], 5)

    def test_get_offer_unauthenticated(self):
        url = offer_detail_url(self.offer.pk)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offer_not_found(self):
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(999)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_patch_offer_success(self):
    #     self.client.force_authenticate(self.owner)
    #     url = offer_detail_url(self.offer.pk)
    #     payload = {
    #         'title': 'Updated Grafikdesign-Paket',
    #         'details': [
    #             {
    #                 'id': self.details[0].id,
    #                 'title': 'Basic Design Updated',
    #                 'revisions': 3,
    #                 'delivery_time_in_days': 6,
    #                 'price': 120,
    #                 'features': ['Logo Design', 'Flyer'],
    #                 'offer_type': 'basic'
    #             }
    #         ]
    #     }
    #     response = self.client.patch(url, payload, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     data = response.data
    #     self.assertEqual(data['title'], 'Updated Grafikdesign-Paket')
    #     # Ensure nested detail updated
    #     updated = next(d for d in data['details']
    #                    if d['id'] == self.details[0].id)
    #     self.assertEqual(updated['title'], 'Basic Design Updated')
    #     # Unchanged detail remains
    #     other = next(d for d in data['details']
    #                  if d['id'] == self.details[1].id)
    #     self.assertEqual(other['title'], 'Standard Design')

    def test_patch_offer_unauthenticated(self):
        url = offer_detail_url(self.offer.pk)
        response = self.client.patch(url, {'title': 'X'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_offer_forbidden(self):
        self.client.force_authenticate(self.other)
        url = offer_detail_url(self.offer.pk)
        response = self.client.patch(url, {'title': 'X'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_offer_not_found(self):
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(999)
        response = self.client.patch(url, {'title': 'X'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_offer_success(self):
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(self.offer.pk)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(pk=self.offer.pk).exists())

    def test_delete_offer_unauthenticated(self):
        url = offer_detail_url(self.offer.pk)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_offer_forbidden(self):
        self.client.force_authenticate(self.other)
        url = offer_detail_url(self.offer.pk)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_not_found(self):
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(999)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
