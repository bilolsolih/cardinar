from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView

from apps.cart.models import CartItem
from .serializers import CartItemListSerializer


class CartItemListAPIView(ListAPIView):
    serializer_class = CartItemListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description='Device id', type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        device_id = self.request.query_params.get('device_id', None)
        if user:
            return CartItem.objects.filter(cart__user=user)
        else:
            return CartItem.objects.filter(device_id=device_id)


__all__ = ['CartItemListAPIView']
