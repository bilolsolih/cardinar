from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.store.models.product import CarCover, Nakidka, Polik


# Create your tests here.


class CarCoverAPITest(TestCase):
    def setUp(self):
        self.url = reverse('constructor:car-cover')
        self.valid_payload = {'name': 'Car Cover 1', 'description': 'A car cover for protection.'}
        self.invalid_payload = {'name': '', 'description': 'A car cover for protection.'}

    def test_carcover_create(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


