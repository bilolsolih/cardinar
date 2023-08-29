from rest_framework import serializers

from django.db import transaction as db_transaction
from django.utils.translation import gettext_lazy as _

from apps.payment.api_endpoints.card.service import KarmonPayClient
from apps.payment.models import Provider, TransactionStatus


class OrderWithCardSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs["provider"] == Provider.CARD:
            if not attrs["user_card"]:
                raise serializers.ValidationError(detail={"user_card": _("This field is required")}, code="required")

            if attrs["user_card"].user != self.context["request"].user:
                raise serializers.ValidationError(detail={"user_card": _("Invalid user card")}, code="invalid")
        return attrs

    def create(self, validated_data):
        if validated_data["provider"] != Provider.CARD:
            return super().create(validated_data)

        with db_transaction.atomic():
            order = super().create(validated_data)
            error, response, transaction = KarmonPayClient().pay(order)

        if error:
            if transaction:
                transaction.status = TransactionStatus.FAILED
                transaction.save()
            if response["error"]["code"] == "insufficient_funds":
                raise serializers.ValidationError(
                    detail={"user_card": _("Insufficient funds")}, code="insufficient_funds"
                )
            elif response["error"]["code"] == "transaction_not_available_for_payment":
                raise serializers.ValidationError(
                    detail={"user_card": _("Transaction not available for payment")},
                    code="transaction_not_available_for_payment",
                )
            else:
                raise serializers.ValidationError(
                    detail={"user_card": _("Something went wrong")}, code="something_went_wrong"
                )

        transaction.apply()
        return order
