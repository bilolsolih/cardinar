from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.utils import timezone

from apps.payment.models import Order
from apps.users.models import User
from apps.webinar.models import UserWebinar, Webinar, WebinarCategory


class WebinarOrderCreateTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(phone="+998935961151", password="12345678")
        self.user2 = User.objects.create_user(phone="+998935961152", password="12345678", email="user@test1.com")
        self.category = WebinarCategory.objects.create(name="test category")

        self.url = reverse("payment:WebinarOrderCreate")

    def test_webinar_order_create_with_valid_data(self):
        webinar = Webinar.objects.create(
            title="test webinar",
            description="test webinar description",
            start_date=timezone.datetime(2021, 1, 1, 0, 0, 0),
            end_date=timezone.now() - timezone.timedelta(hours=20),
            status="waiting",
            category=self.category,
            owner=self.user1,
            price=1000.00,
        )
        data = {"webinar": webinar.id, "payment_type": "one_time", "provider": "uzum_bank", "total_amount": 1000.00}
        expected_data = {
            "webinar": webinar.id,
            "payment_type": "one_time",
            "provider": "uzum_bank",
            "user_card": None,
            "total_amount": "1000.00",
        }
        self.client.login(phone="+998935961152", password="12345678")
        response = self.client.post(self.url, data)
        response.json().pop("id")
        response.json().pop("payment_url")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), expected_data)

    def test_webinar_order_create_with_invalid_amount(self):
        webinar = Webinar.objects.create(
            title="test webinar",
            description="test webinar description",
            start_date=timezone.datetime(2021, 1, 1, 0, 0, 0),
            end_date=timezone.now() - timezone.timedelta(hours=20),
            status="waiting",
            category=self.category,
            owner=self.user1,
            price=1000.00,
        )
        data = {"webinar": webinar.id, "payment_type": "one_time", "provider": "uzum_bank", "total_amount": 100.00}
        error_data = {
            "status_code": 400,
            "errors": [{"error": "total_amount_invalid", "message": "Invalid total amount"}],
        }

        self.client.login(phone="+998935961152", password="12345678")
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), error_data)

    def test_webinar_order_create_for_bought_webinar(self):
        webinar = Webinar.objects.create(
            title="test webinar",
            description="test webinar description",
            start_date=timezone.datetime(2021, 1, 1, 0, 0, 0),
            end_date=timezone.now() - timezone.timedelta(hours=20),
            status="waiting",
            category=self.category,
            owner=self.user1,
            price=1000.00,
        )
        order = Order.objects.create(
            user=self.user2,
            type="webinar",
            webinar=webinar,
            payment_type="one_time",
            provider="uzum_bank",
            total_amount=1000.00,
            is_paid=True,
        )
        UserWebinar.objects.create(user=self.user2, webinar=webinar, order=order)
        data = {"webinar": webinar.id, "payment_type": "one_time", "provider": "uzum_bank", "total_amount": 1000.00}
        error_data = {
            "status_code": 400,
            "errors": [{"error": "webinar_already_bought", "message": "You have already bought this webinar"}],
        }

        self.client.login(phone="+998935961152", password="12345678")
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), error_data)

    def test_webinar_order_create_for_finished_webinar(self):
        webinar = Webinar.objects.create(
            title="test webinar",
            description="test webinar description",
            start_date=timezone.datetime(2021, 1, 1, 0, 0, 0),
            end_date=timezone.now() - timezone.timedelta(hours=20),
            status="finished",
            category=self.category,
            owner=self.user1,
            price=1000.00,
        )
        data = {"webinar": webinar.id, "payment_type": "one_time", "provider": "uzum_bank", "total_amount": 1000.00}
        error_data = {
            "status_code": 400,
            "errors": [{"error": "webinar_is_finished", "message": "This webinar is finished"}],
        }
        self.client.login(phone="+998935961152", password="12345678")
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), error_data)

    def test_webinar_order_create_for_finished_webinar_can_bought(self):
        webinar = Webinar.objects.create(
            title="test webinar",
            description="test webinar description",
            start_date=timezone.datetime(2021, 1, 1, 0, 0, 0),
            end_date=timezone.now() - timezone.timedelta(hours=20),
            status="finished",
            category=self.category,
            owner=self.user1,
            price=1000.00,
            can_be_bought_after_finish=True,
        )
        data = {"webinar": webinar.id, "payment_type": "one_time", "provider": "uzum_bank", "total_amount": 1000.00}
        expected_data = {
            "webinar": webinar.id,
            "payment_type": "one_time",
            "provider": "uzum_bank",
            "user_card": None,
            "total_amount": "1000.00",
        }
        self.client.login(phone="+998935961152", password="12345678")
        response = self.client.post(self.url, data)
        response.json().pop("id")
        response.json().pop("payment_url")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), expected_data)
