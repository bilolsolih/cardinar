from rest_framework.generics import ListAPIView

from apps.orders.models import OrderItem
from .serializers import OrderItemListSerializer


class OrderItemListAPIView(ListAPIView):
    serializer_class = OrderItemListSerializer
    queryset = OrderItem.objects.all()
    lookup_field = 'order_id'


__all__ = ['OrderItemListAPIView']
