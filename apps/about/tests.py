from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Address, Email, SocialMedia, PhoneNumber


class AboutTestCase(TestCase):
    fixtures = [
        'fixtures/about/phone_numbers',
        'fixtures/about/social_medias',
        'fixtures/about/addresses',
        # 'fixtures/about/banners',
        'fixtures/about/emails',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()

    def test_addresses(self):
        response = self.api_client.get(reverse("about:address_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        fields = ['region', 'district', 'street', 'house_no']
        for field in fields:
            self.assertContains(response, field, count=Address.objects.count())

    def test_emails(self):
        response = self.api_client.get(reverse("about:email_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertContains(response, 'email', count=Email.objects.count())

    def test_phone_numbers(self):
        response = self.api_client.get(reverse("about:phone_number_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertContains(response, 'phone_number', count=PhoneNumber.objects.count())

    def test_social_medias(self):
        response = self.api_client.get(reverse("about:social_media_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        fields = ['social_media', 'link']
        for field in fields:
            self.assertContains(response, field, count=SocialMedia.objects.count())
