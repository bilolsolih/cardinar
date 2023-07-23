from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order
from .serializer import OrderListSerializer


class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


__all__ = ['OrderListAPIView']
