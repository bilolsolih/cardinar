from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from django.db import transaction
from django.utils.decorators import method_decorator

from apps.payment.api_endpoints.order.WebinarOrderCreate.serializers import (
    WebinarOrderCreateSerializer,
)
from apps.payment.models import Order, OrderType


@method_decorator(transaction.non_atomic_requests, name="dispatch")
class WebinarOrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = WebinarOrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, type=OrderType.WEBINAR)
