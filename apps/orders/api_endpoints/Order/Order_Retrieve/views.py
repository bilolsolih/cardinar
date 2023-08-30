from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order
from .serializers import OrderRetrieveSerializer


class OrderRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderRetrieveSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


__all__ = ['OrderRetrieveAPIView']
