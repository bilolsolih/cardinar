from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from django.utils.translation import gettext_lazy as _

from .serializers import CheckPromoCodeSerializer

from apps.payment.models import PromoCode


class CheckPromoCodeAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PromoCode.objects.all()
    serializer_class = CheckPromoCodeSerializer
    lookup_field = "code"
    lookup_url_kwarg = "code"

    def get_object(self):
        obj = super().get_object()
        if obj.is_used:
            raise ValidationError(detail={"promo_code": _("Promo code is used")}, code="used")
        if not obj.is_active:
            raise ValidationError(detail={"promo_code": _("Promo code is not active")}, code="not_active")
        return obj
