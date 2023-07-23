from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.cart.models import CartItem
from .serializers import CartItemListSerializer


class CartItemListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemListSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.request.user.cart)


__all__ = ['CartItemListAPIView']
