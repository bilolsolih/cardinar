from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.cart.models import CartItem
from .custom_permission import IsTheOwner
from .serializers import CartItemUpdateSerializer


class CartItemUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTheOwner]
    serializer_class = CartItemUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CartItem.objects.filter(cart__user=user)
        else:
            return None


__all__ = ['CartItemUpdateAPIView']
