from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import CartItemCreateSerializer


class CartItemCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemCreateSerializer

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)


__all__ = ['CartItemCreateAPIView']
