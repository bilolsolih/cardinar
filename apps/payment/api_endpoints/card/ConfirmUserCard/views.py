from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .serializers import ConfirmUserCardSerializer

from apps.payment.api_endpoints.card.service import KarmonPayClient
from apps.payment.models import UserCard


class ConfirmUserCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ConfirmUserCardSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ConfirmUserCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_card = self.check_and_get_user_card(serializer.validated_data["card_number"])
        with db_transaction.atomic():
            error, response = KarmonPayClient().confirm_user_card(
                user=self.request.user,
                card_id=user_card.card_id,
                card_number=serializer.validated_data["card_number"],
                otp=serializer.validated_data["otp"],
                session=serializer.validated_data["session"],
            )
        if error:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_200_OK)

    def check_and_get_user_card(self, card_number):
        user_card = get_object_or_404(UserCard, card_number=card_number, user=self.request.user)
        if user_card.confirmed:
            raise ValidationError(detail={"card_number": _("This card is already confirmed")}, code="confirmed")
        return user_card


__all__ = ["ConfirmUserCardAPIView"]
