import os.path

from rest_framework import status
from rest_framework.test import APITestCase

from django.conf import settings
from django.core.files import File
from django.urls import reverse

from apps.course.models import (
    Course,
    CourseCategory,
    CourseType,
    UserVideoLesson,
    VideoLesson,
)
from apps.payment.models import Order, OrderType, Provider
from apps.users.models import User


class VideoLessonOrderCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("payment:VideoLessonOrderCreate")
        self.category = CourseCategory.objects.create(title="test")
        with File(open(os.path.join(settings.BASE_DIR, "test_files/image.png"), "rb")) as image:
            course = Course(
                title="test",
                description="test",
                category=self.category,
                cover_image=image,
                trailer_video="https://www.youtube.com/watch?v=aTjPyTjso_U",
                type=CourseType.VIDEO_SALE,
                one_time_price=1000,
                two_time_price=2000,
                four_time_price=4000,
            )
            course.cover_image.save("image.png", image, save=False)
            course.save()

            self.video_lesson = VideoLesson(
                title="test",
                course=course,
                video="https://www.youtube.com/watch?v=aTjPyTjso_U",
                cover_image=image,
                one_time_price=1000,
                two_time_price=2000,
                four_time_price=4000,
            )
            self.video_lesson.cover_image.save("image.png", image, save=True)

    def test_create_order_with_valid_data(self):
        user = User.objects.create_user(phone="+998977777777", password="strongPWD")
        data = {
            "video_lesson": self.video_lesson.id,
            "payment_type": "one_time",
            "provider": "uzum_bank",
            "total_amount": 1000,
        }
        expected_data = {
            "video_lesson": self.video_lesson.id,
            "payment_type": "one_time",
            "provider": "uzum_bank",
            "total_amount": "1000.00",
            "user_card": None,
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, data=data)
        response.json().pop("id")
        response.json().pop("payment_url")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), expected_data)

    def test_create_order_with_invalid_amount(self):
        user = User.objects.create_user(phone="+998977777777", password="strongPWD")
        data = {
            "video_lesson": self.video_lesson.id,
            "payment_type": "one_time",
            "provider": "uzum_bank",
            "total_amount": 100,
        }
        expected_data = {
            "status_code": 400,
            "errors": [{"error": "total_amount_invalid", "message": "Invalid total amount"}],
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), expected_data)

    def test_create_order_with_bought_video_lesson(self):
        user = User.objects.create_user(phone="+998977777777", password="strongPWD")
        data = {
            "video_lesson": self.video_lesson.id,
            "payment_type": "one_time",
            "provider": "uzum_bank",
            "total_amount": 1000,
        }
        expected_data = {
            "status_code": 400,
            "errors": [
                {"error": "video_lesson_already_bought", "message": "You have already bought this video lesson"}
            ],
        }
        order = Order.objects.create(
            user=user,
            video_lesson=self.video_lesson,
            total_amount=1000,
            type=OrderType.VIDEO_LESSON,
            payment_type="one_time",
            provider=Provider.UZUM_BANK,
        )
        UserVideoLesson.objects.create(user=user, video_lesson=self.video_lesson, order=order)
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), expected_data)
