from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from django.db import transaction as db_transaction
from django.utils.translation import gettext_lazy as _

from apps.common.models import Setting
from apps.payment.api_endpoints.click.auth import authentication
from apps.payment.api_endpoints.click.Complete.serializers import (
    ClickCompleteSerializer,
)
from apps.payment.api_endpoints.click.provider import ClickProvider
from apps.payment.models import OrderType, Provider, TransactionStatus
from apps.payment.views import PaymentView


class ClickCompleteAPIView(PaymentView):
    TYPE = "complete"
    PROVIDER = Provider.CLICK  # type: ignore

    @swagger_auto_schema(request_body=ClickCompleteSerializer)
    def post(self, request, *args, **kwargs):
        check_auth = authentication(request)
        if not check_auth:
            return Response({"error": "-1", "error_note": _("SIGN CHECK FAILED!")})
        serializer = ClickCompleteSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)

        with db_transaction.atomic():
            click_provider = ClickProvider(serializer.validated_data)
            response = click_provider.complete()

        response["fiscal_items"] = list()

        if click_provider.has_transaction:
            transaction = click_provider.transaction
        else:
            transaction = None

        response["click_trans_id"] = serializer.validated_data.get("click_trans_id", None)
        response["merchant_trans_id"] = serializer.validated_data.get("merchant_trans_id", None)
        response["merchant_prepare_id"] = serializer.validated_data.get("merchant_prepare_id", None)
        response["merchant_confirm_id"] = serializer.validated_data.get("merchant_prepare_id", None)

        if response["error"] == "0":
            transaction = click_provider.transaction

            with db_transaction.atomic():
                transaction.apply()
                self.add_fiscal_data(response, transaction)
            return Response(response)

        if transaction and transaction.status == TransactionStatus.WAITING:
            transaction.status = TransactionStatus.FAILED
            transaction.save()

        return Response(response)

    @staticmethod
    def add_fiscal_data(response, transaction):
        response["received_cash"] = 0
        response["received_ecash"] = 0
        response["received_card"] = transaction.amount * 100

        if transaction.order.type == OrderType.COURSE:
            product_name = transaction.order.course.title
        elif transaction.order.type == OrderType.VIDEO_LESSON:
            product_name = transaction.order.video_lesson.title
        elif transaction.order.type == OrderType.WEBINAR:
            product_name = transaction.order.webinar.title
        else:
            product_name = str(transaction.order.id)
        sett = Setting.objects.last()
        response["fiscal_items"].append(
            {
                "Name": product_name,
                "SPIC": str(sett.soliq_spic),
                "GoodPrice": transaction.amount * 100,
                "Units": 1,
                "Amount": 1,
                "code": str(sett.soliq_service_code),
                "PackageCode": str(sett.soliq_package_code),
                "VAT": transaction.amount * sett.soliq_nds,
                "VATPercent": sett.soliq_nds,
                "CommissionInfo": {"TIN": str(sett.soliq_inn)},
            }
        )
