from os import getenv

from asgiref.sync import async_to_sync
from rest_framework.generics import CreateAPIView
from telegram import Bot
from telegram.error import NetworkError

from apps.users.models import TelegramUser
from .serializers import InquiryCreateSerializer


class InquiryCreateAPIView(CreateAPIView):
    serializer_class = InquiryCreateSerializer

    @staticmethod
    def send_message_to_users(message):
        bot = Bot(token=getenv('BOT_TOKEN'))
        for user in TelegramUser.objects.filter(active=True):
            async_to_sync(bot.send_message)(chat_id=user.chat_id, text=message)

    def perform_create(self, serializer):
        q = serializer.save()
        header = f"️Новый запрос: {q.pk}\n\n" if not q.is_one_click else "❗️❗️❗️Новый Buy-One-Click запрос❗️️❗️❗️\n\n"
        full_name = f"Полное имя: {q.full_name}\n"
        phone_number = f"Телефон: {q.phone_number}\n"
        email = f"Почта: {q.email}\n" if q.email else "\n"
        product_details = f"ID: {q.on_product.pk}, Название: {q.on_product.title}, Категория: {q.on_product.category.title}\n" if q.on_product else "\n"
        articul = f"Артикуль: {q.articul.title}\nМодель автомобиля: {q.articul.car_model.title}\n" if q.articul else "\n"
        comment = f"Коммент: {q.comment}\n"

        message = f"{header} {full_name} {phone_number} {email} {product_details} {articul} {comment}"
        try:
            self.send_message_to_users(message)
        except NetworkError as e:
            if 'Event loop is closed' in str(e):
                pass
            else:
                raise ValueError('Some error happened which is not that Event loop closed error!')
