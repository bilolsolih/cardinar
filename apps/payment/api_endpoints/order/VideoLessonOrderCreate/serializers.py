from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from apps.payment.api_endpoints.order.serializer import OrderWithCardSerializer
from apps.payment.models import Order, PaymentType, UserVideoLesson


class VideoLessonOrderCreateSerializer(OrderWithCardSerializer):
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "video_lesson", "payment_type", "provider", "user_card", "total_amount", "payment_url")
        extra_kwargs = {"video_lesson": {"required": True}}

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["course"] = attrs["video_lesson"].course
        if UserVideoLesson.objects.filter(
            video_lesson=attrs["video_lesson"], user=self.context["request"].user
        ).exists():
            raise serializers.ValidationError(
                detail={"video_lesson": _("You have already bought this video lesson")}, code="already_bought"
            )
        self.check_total_amount(attrs)
        return attrs

    def check_total_amount(self, attrs):
        if attrs["payment_type"] == PaymentType.ONE_TIME:
            total_amount = attrs["video_lesson"].one_time_price
            if attrs["video_lesson"].sale:
                total_amount = attrs["video_lesson"].sale.one_time_price
        elif attrs["payment_type"] == PaymentType.TWO_TIME:
            total_amount = attrs["video_lesson"].two_time_price * 2
            if attrs["video_lesson"].sale:
                total_amount = attrs["video_lesson"].sale.two_time_price * 2
        elif attrs["payment_type"] == PaymentType.FOUR_TIME:
            total_amount = attrs["video_lesson"].four_time_price * 4
            if attrs["video_lesson"].sale:
                total_amount = attrs["video_lesson"].sale.four_time_price * 4
        else:
            raise serializers.ValidationError(detail={"payment_type": _("Invalid payment type")}, code="invalid")

        if total_amount != attrs["total_amount"]:
            raise serializers.ValidationError(detail={"total_amount": _("Invalid total amount")}, code="invalid")

    def get_payment_url(self, obj):
        return obj.get_payment_url()
