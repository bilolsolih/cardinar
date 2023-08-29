from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from django.conf import settings
from django.db import transaction as db_transaction

from .serializers import ApelsinPaySerializer

from apps.payment.api_endpoints.uzum_bank.provider import ApelsinProvider
from apps.payment.authentication import CustomBasicAuthentication
from apps.payment.models import Provider, Transaction, TransactionStatus
from apps.payment.permissions import IsAuthenticatedAndServerUser
from apps.payment.views import PaymentView


class ApelsinPayAPIView(PaymentView):
    authentication_classes = [
        CustomBasicAuthentication.from_settings(
            settings.PROVIDERS["uzum_bank"]["username"], settings.PROVIDERS["uzum_bank"]["password"]
        )
    ]
    permission_classes = [IsAuthenticatedAndServerUser]
    TYPE = "pay"
    PROVIDER = Provider.UZUM_BANK  # type: ignore

    @swagger_auto_schema(request_body=ApelsinPaySerializer)
    def post(self, request, *args, **kwargs):
        serializer = ApelsinPaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with db_transaction.atomic():
            error, error_message, order = ApelsinProvider(serializer.validated_data["cabinetId"]).pay_info(
                serializer.validated_data["transaction_id"], serializer.validated_data["amount"] / 100
            )

        if not order and error:
            return Response({"status": False, "message": error_message}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction.objects.get(order=order, transaction_id=serializer.validated_data["transaction_id"])

        if error:
            transaction.status = TransactionStatus.FAILED
            transaction.save()
            return Response({"status": False, "message": error_message}, status=status.HTTP_400_BAD_REQUEST)

        with db_transaction.atomic():
            transaction.apply()

        return Response({"status": True}, status=status.HTTP_200_OK)
