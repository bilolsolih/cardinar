from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from apps.payment.api_endpoints.order.serializer import OrderWithCardSerializer
from apps.payment.models import Order, PaymentType
from apps.webinar.models import UserWebinar


class WebinarOrderCreateSerializer(OrderWithCardSerializer):
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "webinar", "payment_type", "provider", "user_card", "total_amount", "payment_url")
        extra_kwargs = {"webinar": {"required": True}}

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs["webinar"].is_free:
            raise serializers.ValidationError(detail={"webinar": _("This webinar is free")}, code="is_free")
        if UserWebinar.objects.filter(webinar=attrs["webinar"], user=self.context["request"].user).exists():
            raise serializers.ValidationError(
                detail={"webinar": _("You have already bought this webinar")}, code="already_bought"
            )
        if attrs["webinar"].status == "finished" and not attrs["webinar"].can_be_bought_after_finish:
            raise serializers.ValidationError(detail={"webinar": _("This webinar is finished")}, code="is_finished")
        self.check_total_amount(attrs)
        return attrs

    def check_total_amount(self, attrs):
        if attrs["payment_type"] == PaymentType.ONE_TIME:
            total_amount = attrs["webinar"].price
        else:
            raise serializers.ValidationError(detail={"payment_type": _("Invalid payment type")}, code="invalid")

        if total_amount != attrs["total_amount"]:
            raise serializers.ValidationError(detail={"total_amount": _("Invalid total amount")}, code="invalid")

    def get_payment_url(self, obj):
        return obj.get_payment_url()
