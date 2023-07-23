from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.cart.models import CartItem
from .custom_permission import IsTheOwner


class CartItemDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTheOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CartItem.objects.filter(cart__user=user)
        else:
            return None


__all__ = ['CartItemDeleteAPIView']
