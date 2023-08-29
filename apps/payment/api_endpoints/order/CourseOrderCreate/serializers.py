from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from apps.course.models import UserCourse
from apps.payment.api_endpoints.order.serializer import OrderWithCardSerializer
from apps.payment.models import Order, PaymentType


class CourseOrderCreateSerializer(OrderWithCardSerializer):
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "course", "payment_type", "provider", "promo_code", "user_card", "total_amount", "payment_url")
        extra_kwargs = {"course": {"required": True}}

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if UserCourse.objects.filter(course=attrs["course"], user=self.context["request"].user).exists():
            raise serializers.ValidationError(
                detail={"course": _("You have already bought this course")}, code="already_bought"
            )
        if attrs.get("promo_code", None):
            promo_code = self.context["promo_code"]
            if promo_code.course != attrs["course"]:
                raise serializers.ValidationError(
                    detail={"promo_code": _("This promo code is not for this course")}, code="invalid"
                )
            if attrs["payment_type"] != PaymentType.ONE_TIME:
                raise serializers.ValidationError(
                    detail={"promo_code": _("Promo code is not for this payment type")}, code="invalid"
                )
        self.check_total_amount(attrs)
        return attrs

    def check_total_amount(self, attrs):
        if attrs["payment_type"] == PaymentType.ONE_TIME:
            total_amount = attrs["course"].one_time_price
            if attrs["course"].sale:
                total_amount = attrs["course"].sale.one_time_price
            if attrs.get("promo_code", None):
                promo_code = self.context["promo_code"]
                total_amount = total_amount - (promo_code.percent * total_amount / 100)
        elif attrs["payment_type"] == PaymentType.TWO_TIME:
            total_amount = attrs["course"].two_time_price * 2
            if attrs["course"].sale:
                total_amount = attrs["course"].sale.two_time_price * 2
        elif attrs["payment_type"] == PaymentType.FOUR_TIME:
            total_amount = attrs["course"].four_time_price * 4
            if attrs["course"].sale:
                total_amount = attrs["course"].sale.four_time_price * 4
        else:
            raise serializers.ValidationError(detail={"payment_type": _("Invalid payment type")}, code="invalid")

        if total_amount != attrs["total_amount"]:
            raise serializers.ValidationError(detail={"total_amount": _("Invalid total amount")}, code="invalid")

    def validate_promo_code(self, value):
        if not value:
            return

        promo_code = self.context["promo_code"]
        if promo_code.is_used:
            raise serializers.ValidationError(detail={"promo_code": _("Promo code is used")}, code="used")
        if not promo_code.is_active:
            raise serializers.ValidationError(detail={"promo_code": _("Promo code is not active")}, code="not_active")
        return value

    def get_payment_url(self, obj):
        return obj.get_payment_url()
