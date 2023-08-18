from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.inquiries.models import Inquiry


class InquiryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()

    def test_inquiry_create_with_email(self):
        full_name = 'Bilol Muhammad Solih'
        phone_number = '+998912958899'
        email = 'Bilol@gmail.com'
        response = self.api_client.post(
            path=reverse('inquiries:inquiry_create'),
            format='json',
            data={
                'full_name': full_name,
                'phone_number': phone_number,
                'email': email
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Inquiry.objects.filter(
            full_name=full_name, phone_number=phone_number, email=email)
        )

    def test_inquiry_create_without_email(self):
        full_name = 'Bilol Solih'
        phone_number = '+998912968899'
        response = self.api_client.post(
            path=reverse('inquiries:inquiry_create'),
            format='json',
            data={
                'full_name': full_name,
                'phone_number': phone_number
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Inquiry.objects.filter(
            full_name=full_name, phone_number=phone_number)
        )
