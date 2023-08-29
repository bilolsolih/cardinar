from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from django.conf import settings
from django.db import transaction as db_transaction

from .serializers import PaylovSerializer
from .utils import PaylovMethods

from apps.payment.api_endpoints.paylov.provider import PaylovProvider
from apps.payment.authentication import CustomBasicAuthentication
from apps.payment.models import Provider, Transaction, TransactionStatus
from apps.payment.permissions import IsAuthenticatedAndServerUser
from apps.payment.views import PaymentView


class PaylovAPIView(PaymentView):
    authentication_classes = [
        CustomBasicAuthentication.from_settings(
            settings.PROVIDERS["karmon_pay"]["username"], settings.PROVIDERS["karmon_pay"]["password"]
        )
    ]
    permission_classes = [IsAuthenticatedAndServerUser]
    http_method_names = ["post"]
    TYPE = ""
    PROVIDER = Provider.KARMON_PAY  # type: ignore

    def __init__(self):
        self.METHODS = {
            PaylovMethods.CHECK_TRANSACTION: self.check,
            PaylovMethods.PERFORM_TRANSACTION: self.perform,
        }
        self.params = None
        self.amount = None
        super(PaylovAPIView, self).__init__()

    @swagger_auto_schema(request_body=PaylovSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PaylovSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)

        method = serializer.validated_data["method"]
        self.params = serializer.validated_data["params"]
        self.TYPE = method

        with db_transaction.atomic():
            response_data = self.METHODS[method]()

        if isinstance(response_data, dict):
            response_data.update({"jsonrpc": "2.0", "id": request.data.get("id", None)})

        return Response(response_data)

    def check(self):
        error, code = PaylovProvider(self.params).check()
        if error:
            return dict(result=dict(status=code, statusText=PaylovProvider.ERROR_STATUS_TEXT))
        return dict(result=dict(status=code, statusText=PaylovProvider.SUCCESS_STATUS_TEXT))

    def perform(self):
        error, code = PaylovProvider(self.params).perform()

        # when order is not found
        if error and code == PaylovProvider.ORDER_NOT_FOUND:
            return dict(result=dict(status=code, statusText=PaylovProvider.ERROR_STATUS_TEXT))

        transaction = Transaction.objects.get(
            transaction_id=self.params["transaction_id"], order__provider=Provider.KARMON_PAY
        )

        # when order found and transaction created but error occurred
        if error:
            transaction.status = TransactionStatus.FAILED
            transaction.save()
            return dict(result=dict(status=code, statusText=PaylovProvider.ERROR_STATUS_TEXT))

        if transaction.status == TransactionStatus.WAITING:
            with db_transaction.atomic():
                transaction.apply()

        return dict(result=dict(status=code, statusText=PaylovProvider.SUCCESS_STATUS_TEXT))
