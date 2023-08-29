from rest_framework import serializers

from apps.payment.models import PromoCode


class CheckPromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ("id", "code", "percent", "course")
