from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..service import KarmonPayClient
from .serializers import UserCardListSerializer

from apps.payment.models import UserCard


class GetUserCardListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCardListSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return UserCard.objects.none()
        return UserCard.objects.filter(user=self.request.user, confirmed=True)

    def get_serializer_context(self):
        if getattr(self, "swagger_fake_view", False):
            return {}
        context = super().get_serializer_context()
        error, response = KarmonPayClient().get_user_cards(str(self.request.user.uuid))
        if error:
            return context
        context.update({"user_card_list": response["result"]["cards"]})
        return context


__all__ = ["GetUserCardListAPIView"]
