from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.payment.api_endpoints.card.service import KarmonPayClient
from apps.payment.models import UserCard


class DeleteUserCardAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserCard.objects.filter(confirmed=True)
    lookup_url_kwarg = "user_card_id"

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_destroy(self, instance):
        KarmonPayClient().delete_user_card(instance.card_id)
        instance.delete()


__all__ = ["DeleteUserCardAPIView"]
