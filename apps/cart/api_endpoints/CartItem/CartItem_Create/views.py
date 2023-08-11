from rest_framework.generics import CreateAPIView

from .serializers import CartItemCreateSerializer


class CartItemCreateAPIView(CreateAPIView):
    serializer_class = CartItemCreateSerializer


__all__ = ['CartItemCreateAPIView']
