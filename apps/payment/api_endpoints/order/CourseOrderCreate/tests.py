from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.course.models import Course, CourseCategory
from apps.users.models import User


class CourseOrderCreateViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(phone="+989123456789", password="12345678")
        self.category = CourseCategory.objects.create(title="test category")
        self.url = reverse("payment:course-order-create")

    def test_valid_course_order_create(self):
        course = Course.objects.create(
            title="test course",
            category=self.category,
            author="test author",
            description="test description",
            one_time_price=1000,
            two_time_price=2000,
            four_time_price=4000,
            type="course_sale",
        )
        data = {
            "course": course.id,
            "payment_type": "one_time",
            "provider": "uzum_bank",
            "total_amount": 1000.00,
        }

        expected_data = {
            "course": course.id,
            "payment_type": "one_time",
            "provider": "uzum_bank",
            "total_amount": "1000.00",
            "promo_code": None,
            "user_card": None,
        }
        self.client.force_login(self.user)
        response = self.client.post(self.url, data)
        response.json().pop("id")
        response.json().pop("payment_url")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), expected_data)

    def test_course_order_create_with_invalid_amount(self):
        course = Course.objects.create(
            title="test course",
            category=self.category,
            author="test author",
            description="test description",
            one_time_price=1000,
            two_time_price=2000,
            four_time_price=4000,
            type="course_sale",
        )
        data = {"course": course.id, "payment_type": "one_time", "provider": "uzum_bank", "total_amount": 100.00}

        error_data = {
            "status_code": 400,
            "errors": [{"error": "total_amount_invalid", "message": "Invalid total amount"}],
        }

        self.client.force_login(self.user)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), error_data)
