from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order
from .serializers import OrderRetrieveSerializer


class OrderRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderRetrieveSerializer
    queryset = Order.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user, pk=self.kwargs.get('pk', None)).first()


__all__ = ['OrderRetrieveAPIView']
