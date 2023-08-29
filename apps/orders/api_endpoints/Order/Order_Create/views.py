from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
import requests
import os
import time

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

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        order = serializer.save(user=user)
        device_id = self.request.query_params.get('device_id', None)
        items = user.cart.items.all() if user else CartItem.objects.filter(device_id=device_id)

        for item in items:
            OrderItem.objects.create(
                order=order, content_type=item.content_type, object_id=item.object_id, quantity=item.quantity, cost=item.cost
            )
        requests.post(
            url='https://test.paycom.uz/create-transaction/',
            data={
                "jsonrpc": "2.0",
                "id": 58882,
                "method": "CreateTransaction",
                "params": {
                    "account": {
                        "order_id": "1"
                    },
                    "amount": 500,
                    "id": "64ec8047bd4e15d6824257df",
                    "time": int(time.time() * 1000)
                }
            }
        )


__all__ = ['OrderCreateAPIView']
