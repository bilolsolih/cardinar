from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.orders.models import OrderItem
from apps.store.models.product import Product
from .serializers import OrderCreateSerializer


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user if self.request.user.is_authenticated else None
        cart = self.request.session.get(settings.CART_SESSION_ID, None)
        if not cart or not cart.items():
            return Response({'detail': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        final_price = 0
        for key, value in cart.items():
            final_price += value['cost']

        order = serializer.save(user=user, final_price=final_price)

        for key in list(cart.keys()):
            product = Product.objects.get(pk=key, active=True)
            OrderItem.objects.create(order=order, product=product, quantity=cart[key]['quantity'], cost=cart[key]['cost'])
            del cart[key]
        self.request.session.modified = True

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


__all__ = ['OrderCreateAPIView']
