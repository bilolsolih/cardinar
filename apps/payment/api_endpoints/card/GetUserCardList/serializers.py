from rest_framework import serializers

from apps.payment.models import UserCard


class UserCardListSerializer(serializers.ModelSerializer):
    card_number = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = UserCard
        fields = ("id", "card_number", "balance")

    def get_card_number(self, obj):
        return f"{obj.card_number[:6]}********{obj.card_number[-2:]}"

    def get_balance(self, obj):
        user_card_list = self.context.get("user_card_list", [])
        if not user_card_list:
            return
        user = self.context["request"].user
        card = list(filter(lambda x: x["userId"] == str(user.uuid) and x["cardId"] == obj.card_id, user_card_list))
        return card[0]["balance"] if card else None
