from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from django.db import transaction as db_transaction

from .serializers import CreateUserCardSerializer

from apps.payment.api_endpoints.card.service import KarmonPayClient


class CustomUserRateThrottle(UserRateThrottle):
    def get_rate(self):
        return "4/minute"


class CreateUserCardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle]

    @swagger_auto_schema(request_body=CreateUserCardSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CreateUserCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        with db_transaction.atomic():
            error, response = KarmonPayClient().create_user_card(
                user=self.request.user,
                user_uuid=str(request.user.uuid),
                card_number=validated_data["card_number"],
                expire_date=validated_data["expire_date"],
            )

        if error:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_200_OK)


__all__ = ["CreateUserCardAPIView"]
