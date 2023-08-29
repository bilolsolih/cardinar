from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from .serializers import GetLastTransactionStatusSerializer

from apps.payment.models import Order


class GetLastTransactionStatusAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = GetLastTransactionStatusSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "order_id"

    def get_object(self):
        order = super().get_object()
        if not order.transaction_set.exists():
            raise Http404
        return order.transaction_set.last()


__all__ = ["GetLastTransactionStatusAPIView"]
