from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from django.db import transaction
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from apps.payment.api_endpoints.order.CourseOrderCreate.serializers import (
    CourseOrderCreateSerializer,
)
from apps.payment.models import Order, OrderType, PromoCode


@method_decorator(transaction.non_atomic_requests, name="dispatch")
class CourseOrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CourseOrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, type=OrderType.COURSE)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.data.get("promo_code", None):
            try:
                context["promo_code"] = PromoCode.objects.get(code=self.request.data.get("promo_code"))
            except PromoCode.DoesNotExist:
                raise ValidationError(detail={"promo_code": _("Promo code does not exist")}, code="not_exist")
        return context
