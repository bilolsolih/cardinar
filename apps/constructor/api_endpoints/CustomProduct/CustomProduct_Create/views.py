import requests
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from apps.constructor.models import CustomProduct
from .serializer import CustomProductCreateSerializer


class CustomProductCreateAPIView(CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CustomProductCreateSerializer
    queryset = CustomProduct.objects.all()

    def perform_create(self, serializer):
        model = serializer.save()

        telegram_bot_token = '6689575443:AAHn148ymq6VL8qVgsLsv-iVVWfLoGOCi4Q'
        chat_id = '-1001915286015'

        message = f"Ф.И.О: {model.full_name}\n"
        message += f"Номер телефона: {model.phone_number}\n"
        message += f"Телеграм: {model.email}\n"
        message += f"Марка Автомобиля: {model.car_model}\n"

        files = {'photo': open(model.photo.path, 'rb')}

        response = requests.post(
            f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto",
            data={'chat_id': chat_id, 'caption': message},
            files=files
        )

        if response.status_code != 200:
            pass


__all__ = ['CustomProductCreateAPIView']
