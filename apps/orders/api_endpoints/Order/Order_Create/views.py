from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.db.models import Sum
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

        for item in items:
            OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity, cost=item.cost, car_model=item.car_model
            )
        for item in items:
            item.delete()

        return order.get_payment_url()


__all__ = ['OrderCreateAPIView']
