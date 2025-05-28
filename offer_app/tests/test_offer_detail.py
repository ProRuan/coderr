# Third-party suppliers
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Local imports
from offer_app.models import Offer, OfferDetail

User = get_user_model()


def offer_detail_url(pk):
    """
    Get URL of an offer.
    """
    return f'/api/offers/{pk}/'


class OfferDetailTests(APITestCase):
    """
    Tests for retrieving, updating and deleting offers.
    """

    def setUp(self):
        """
        Set up owner, other user and offer.
        """
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username='owner', email='owner@example.com',
            password='pass', type='business'
        )
        self.other = User.objects.create_user(
            username='other', email='other@example.com',
            password='pass', type='business'
        )
        self.offer = Offer.objects.create(
            user=self.owner,
            title='Grafikdesign-Paket',
            description='Ein umfassendes Grafikdesign-Paket.'
        )
        self.details = []
        for idx, title in enumerate(['Basic', 'Standard', 'Premium'], 1):
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
        """
        Ensure authenticated owner can retrieve their offer (HTTP 200).
        """
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(self.offer.pk)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['id'], self.offer.pk)
        self.assertEqual(len(data['details']), 3)

    def test_get_offer_unauthenticated(self):
        """
        Ensure unauthenticated users cannot retrieve offer (HTTP 401).
        """
        url = offer_detail_url(self.offer.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offer_not_found(self):
        """
        Ensure HTTP 404 is returned for non-existing offer.
        """
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(999)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_offer_success(self):
        """
        Ensure authenticated owner can update offer (HTTP 200).
        """
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(self.offer.pk)
        payload = {
            'title': 'Updated Paket',
            'details': [{
                'id': self.details[0].id,
                'title': 'Basic Design Updated',
                'revisions': 3,
                'delivery_time_in_days': 6,
                'price': 120,
                'features': ['Logo', 'Flyer'],
                'offer_type': 'basic'
            }]
        }
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.data
        updated = next(d for d in data['details']
                       if d['id'] == self.details[0].id)
        self.assertEqual(updated['title'], 'Basic Design Updated')

    def test_patch_offer_unauthenticated(self):
        """
        Ensure unauthenticated users cannot update offer (HTTP 401).
        """
        url = offer_detail_url(self.offer.pk)
        res = self.client.patch(url, {'title': 'X'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_offer_forbidden(self):
        """
        Ensure other users cannot update someone else's offer (HTTP 403).
        """
        self.client.force_authenticate(self.other)
        url = offer_detail_url(self.offer.pk)
        res = self.client.patch(url, {'title': 'X'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_offer_not_found(self):
        """
        Ensure updating a non-existent offer returns HTTP 404.
        """
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(999)
        res = self.client.patch(url, {'title': 'X'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_offer_success(self):
        """
        Ensure owner can successfully delete their offer (HTTP 204).
        """
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(self.offer.pk)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(pk=self.offer.pk).exists())

    def test_delete_offer_unauthenticated(self):
        """
        Ensure unauthenticated users cannot delete offers (HTTP 401).
        """
        url = offer_detail_url(self.offer.pk)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_offer_forbidden(self):
        """
        Ensure non-owners cannot delete someone else's offer (HTTP 403).
        """
        self.client.force_authenticate(self.other)
        url = offer_detail_url(self.offer.pk)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_not_found(self):
        """
        Ensure deleting a non-existent offer returns HTTP 404.
        """
        self.client.force_authenticate(self.owner)
        url = offer_detail_url(999)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
