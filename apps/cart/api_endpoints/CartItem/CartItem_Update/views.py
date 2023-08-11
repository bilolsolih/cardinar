from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.cart.models import CartItem
from .serializers import CartItemUpdateSerializer


class CartItemUpdateAPIView(UpdateAPIView):
    serializer_class = CartItemUpdateSerializer
    queryset = CartItem.objects.all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description='Device id', type=openapi.TYPE_STRING),
        ]
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        item = serializer.save()
        item.cost = item.quantity * item.product.price
        item.save()

    def get_object(self):
        user = self.request.user
        device_id = self.request.query_params.get('device_id', None)
        if user.is_authenticated and device_id:
            raise ValueError('device_id is needed only for guest users.')
        if user.is_authenticated:
            return CartItem.objects.filter(cart__user=user, pk=self.kwargs.get('pk', None)).first()
        else:
            return CartItem.objects.filter(device_id=device_id, pk=self.kwargs.get('pk', None)).first()


__all__ = ['CartItemUpdateAPIView']
