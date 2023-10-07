import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from apps.cart.models import CartItem
from apps.orders.models import OrderItem
from .serializers import OrderCreateSerializer


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('device_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_url = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': serializer.data, 'payment_url': payment_url}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        order = serializer.save(user=user)
        device_id = self.request.query_params.get('device_id', None)
        items = user.cart.items.all() if user else CartItem.objects.filter(device_id=device_id)

        order_message = f"Order {order.id}:\n"
        order_message += f"Full Name: {order.full_name}\n"
        order_message += f"Phone Number: {order.phone_number}\n"
        order_message += f"Email: {order.email}\n"
        if order.delivery_type == 's':
            order_message += "Способ доставки: Самовывоз\n"
        else:
            order_message += "Способ доставки: Доставка\n"
            order_message += f"Город: {order.city}\n"
            order_message += f"Регион: {order.region}\n"
            order_message += f"Адрес: {order.address}\n"
            order_message += f"Этаж: {order.level}\n"
        order_message += f"Способ оплаты: {order.payment_method}\n"
        order_message += f"Цена: {order.store}\n"

        photos = []

        for item in items:
            OrderItem.objects.create(
                order=order, product=item.product, articul=item.articul, quantity=item.quantity, cost=item.cost, car_model=item.car_model
            )
            photos.append(('photo', item.photo.photo.file))
        for item in items:
            item.delete()

        telegram_bot_token = '6689575443:AAHn148ymq6VL8qVgsLsv-iVVWfLoGOCi4Q'
        chat_id = '-1001915286015'

        response = requests.post(
            f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto",
            data={'chat_id': chat_id, 'caption': order_message},
            files=photos
        )

        if response.status_code != 200:
            pass

        return order.get_payment_url()


__all__ = ['OrderCreateAPIView']
