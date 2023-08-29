from django.utils.translation import gettext_lazy as _

from apps.course.models import UserCourse, UserVideoLesson
from apps.payment.models import (
    Order,
    OrderType,
    PaymentType,
    Provider,
    Transaction,
    TransactionStatus,
)
from apps.webinar.models import UserWebinar


class ClickProvider:
    def __init__(self, data):
        self.data = data
        self.click_trans_id = self.data.get("click_trans_id", None)
        self.service_id = self.data.get("service_id", None)
        self.click_paydoc_id = self.data.get("click_paydoc_id", None)
        self.order_id = self.data.get("merchant_trans_id", None)
        self.amount = self.data.get("amount", None)
        self.action = self.data.get("action", None)
        self.error = self.data.get("error", None)
        self.error_note = self.data.get("error_note", None)
        self.sign_time = self.data.get("sign_time", None)
        self.sign_string = self.data.get("sign_string", None)
        self.merchant_prepare_id = self.data.get("merchant_prepare_id", None) if self.action == 1 else ""
        self.order = self.get_order()
        self.success_response = {"error": "0", "error_note": "Success"}
        self.transaction_found = False
        self.transaction = None

    def prepare(self):
        if self.action != 0:
            return {"error": "-3", "error_note": _("Action not found")}

        if not self.order:
            return {"error": "-5", "error_note": _("Order does not exist")}

        check_order, error_response = self.check_order()
        if not check_order:
            return error_response

        check_order_type, error_response = self.check_order_type()
        if not check_order_type:
            return error_response

        # check transaction exist and create if not exist
        can_prepare_transaction, error_response = self.can_prepare_transaction()
        if not can_prepare_transaction:
            return error_response

        # check amount when can_prepare_transaction is True
        is_valid_amount, error_response = self.is_valid_amount()
        if not is_valid_amount:
            return error_response

        return self.success_response

    def complete(self):
        if self.action != 1:
            return {"error": "-3", "error_note": _("Action not found")}

        if not self.order:
            return {"error": "-5", "error_note": _("Order does not exist")}

        check_order, error_response = self.check_order()
        if not check_order:
            return error_response

        check_order_type, error_response = self.check_order_type()
        if not check_order_type:
            return error_response

        can_complete_transaction, error_response = self.can_complete_transaction()
        if not can_complete_transaction:
            return error_response

        # check amount when can_prepare_transaction is True
        is_valid_amount, error_response = self.is_valid_amount()
        if not is_valid_amount:
            return error_response

        return self.success_response

    def can_complete_transaction(self):
        try:
            transaction = Transaction.objects.get(id=self.merchant_prepare_id)
            # set transaction and transaction_found if transaction exist
            self.transaction_found = True
            self.transaction = transaction
            if transaction.transaction_id != str(self.click_trans_id):
                return False, {"error": "-8", "error_note": _("Transaction ID not match")}
        except Transaction.DoesNotExist:
            return False, {"error": "-7", "error_note": _("Transaction not found")}

        is_valid_status, error_response = self.check_transaction_status()
        if not is_valid_status:
            return False, error_response

        return True, self.success_response

    def can_prepare_transaction(self):
        transaction = self.get_transaction()
        self.transaction_found = True
        self.transaction = transaction

        is_valid_status, error_response = self.check_transaction_status()
        if not is_valid_status:
            return False, error_response

        return True, self.success_response

    def check_transaction_status(self):
        if self.transaction.status == TransactionStatus.PAID:
            return False, {"error": "-4", "error_note": _("Already paid")}
        elif self.transaction.status in [TransactionStatus.CANCELED, TransactionStatus.FAILED]:
            return False, {"error": "-9", "error_note": _("Transaction cancelled or failed")}
        return True, self.success_response

    def get_transaction(self):
        transaction, created = Transaction.objects.get_or_create(
            order_id=self.order_id,
            transaction_id=self.click_trans_id,
            order__provider=Provider.CLICK,
            defaults={"amount": self.amount, "status": TransactionStatus.WAITING},
        )
        return transaction

    @property
    def has_transaction(self):
        return self.transaction_found

    def is_valid_amount(self):
        transaction = Transaction.objects.get(
            order_id=self.order_id, transaction_id=self.click_trans_id, order__provider=Provider.CLICK
        )
        if self.amount != transaction.order.transaction_amount:
            return False, {"error": "-2", "error_note": _("Incorrect parameter amount")}

        return True, self.success_response

    def get_order(self):
        try:
            return Order.objects.get(id=self.order_id)
        except Order.DoesNotExist:
            return

    def check_order(self):
        if self.order.is_paid:
            return False, {"error": "-4", "error_note": _("Already paid")}
        if self.order.payment_type != PaymentType.ONE_TIME:
            return False, {"error": "-6", "error_note": _("Invalid payment type")}
        return True, self.success_response

    def check_order_type(self):
        if self.order.type == OrderType.COURSE:
            if UserCourse.objects.filter(course=self.order.course, user=self.order.user, order=self.order).exists():
                return False, {"error": "-4", "error_note": _("Already paid")}
        elif self.order.type == OrderType.WEBINAR:
            if UserWebinar.objects.filter(webinar=self.order.webinar, user=self.order.user, order=self.order).exists():
                return False, {"error": "-4", "error_note": _("Already paid")}
        elif self.order.type == OrderType.VIDEO_LESSON:
            if UserVideoLesson.objects.filter(
                video_lesson=self.order.video_lesson, user=self.order.user, order=self.order
            ).exists():
                return False, {"error": "-4", "error_note": _("Already paid")}
        return True, self.success_response
