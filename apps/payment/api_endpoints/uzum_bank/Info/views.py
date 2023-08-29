from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from django.conf import settings
from django.db import transaction as db_transaction

from .serializers import ApelsinInfoSerializer

from apps.payment.api_endpoints.uzum_bank.provider import ApelsinProvider
from apps.payment.authentication import CustomBasicAuthentication
from apps.payment.models import Provider
from apps.payment.permissions import IsAuthenticatedAndServerUser
from apps.payment.views import PaymentView


class ApelsinInfoAPIView(PaymentView):
    authentication_classes = [
        CustomBasicAuthentication.from_settings(
            settings.PROVIDERS["uzum_bank"]["username"], settings.PROVIDERS["uzum_bank"]["password"]
        )
    ]
    permission_classes = [IsAuthenticatedAndServerUser]
    TYPE = "info"
    PROVIDER = Provider.UZUM_BANK  # type: ignore

    @swagger_auto_schema(request_body=ApelsinInfoSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ApelsinInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with db_transaction.atomic():
            error, error_message, order = ApelsinProvider(serializer.validated_data["cabinetId"]).get_order_info()
        if error:
            return Response({"status": False, "message": error_message}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "status": True,
            "error": error,
            "data": {
                "full_name": order.user.full_name,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "cabinetId": order.id,
                "amount": float(order.transaction_amount),
            },
        }

        return Response(data, status=status.HTTP_200_OK)
