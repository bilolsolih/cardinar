from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from django.db import transaction as db_transaction
from django.utils.translation import gettext_lazy as _

from .serializers import ClickPrepareSerializer

from apps.payment.api_endpoints.click.auth import authentication
from apps.payment.api_endpoints.click.provider import ClickProvider
from apps.payment.models import Provider, TransactionStatus
from apps.payment.views import PaymentView


class ClickPrepareAPIView(PaymentView):
    TYPE = "prepare"
    PROVIDER = Provider.CLICK  # type: ignore

    @swagger_auto_schema(request_body=ClickPrepareSerializer)
    def post(self, request, *args, **kwargs):
        check_auth = authentication(request)
        if not check_auth:
            return Response({"error": "-1", "error_note": _("SIGN CHECK FAILED!")})
        serializer = ClickPrepareSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)

        with db_transaction.atomic():
            click_provider = ClickProvider(serializer.validated_data)
            response = click_provider.prepare()

        if click_provider.has_transaction:
            transaction = click_provider.transaction
        else:
            transaction = None

        response["click_trans_id"] = serializer.validated_data.get("click_trans_id", None)
        response["merchant_trans_id"] = serializer.validated_data.get("merchant_trans_id", None)

        if response["error"] == "0":
            transaction = click_provider.transaction
            response["merchant_prepare_id"] = transaction.id
            return Response(response)

        if transaction and transaction.status == TransactionStatus.WAITING:
            transaction.status = TransactionStatus.FAILED
            transaction.save()

        return Response(response)
