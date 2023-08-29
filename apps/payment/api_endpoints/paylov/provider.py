from apps.course.models import UserCourse, UserVideoLesson
from apps.payment.models import (
    Order,
    OrderType,
    PaymentType,
    Transaction,
    TransactionStatus,
)
from apps.webinar.models import UserWebinar


class PaylovProvider:
    ORDER_NOT_FOUND = "303"
    ORDER_ALREADY_PAID = "201"
    INVALID_AMOUNT = "5"
    SERVER_ERROR = "3"

    SUCCESS = "0"
    SUCCESS_STATUS_TEXT = "OK"
    ERROR_STATUS_TEXT = "ERROR"

    def __init__(self, params):
        self.params = params
        self.code = self.SUCCESS
        self.error = False
        self.order = self.get_order()

    def perform(self):
        if not self.order:
            return True, self.ORDER_NOT_FOUND

        transaction, _ = Transaction.objects.get_or_create(
            transaction_id=self.params["transaction_id"],
            order=self.order,
            defaults={"amount": self.params["amount"], "status": TransactionStatus.WAITING},
        )

        if transaction.status == TransactionStatus.FAILED:
            return True, self.SERVER_ERROR

        self.validate_order()
        self.validate_amount(self.params["amount"])

        return self.error, self.code

    def check(self):
        if not self.order:
            return True, self.ORDER_NOT_FOUND

        self.validate_order()
        self.validate_amount(self.params["amount"])

        return self.error, self.code

    def get_order(self):
        if not self.params.get("account"):
            return
        try:
            return Order.objects.get(id=self.params["account"]["order_id"])
        except Order.DoesNotExist:
            return

    def validate_order(self):
        if self.order.is_paid:
            self.error = True
            self.code = self.ORDER_ALREADY_PAID
        if self.order.payment_type != PaymentType.ONE_TIME:
            self.error = True
            self.code = self.SERVER_ERROR
        self.validate_order_type()

    def validate_order_type(self):
        if self.order.type == OrderType.COURSE:
            if UserCourse.objects.filter(course=self.order.course, user=self.order.user, order=self.order).exists():
                self.error = True
                self.code = self.ORDER_ALREADY_PAID
        elif self.order.type == OrderType.WEBINAR:
            if UserWebinar.objects.filter(webinar=self.order.webinar, user=self.order.user, order=self.order).exists():
                self.error = True
                self.code = self.ORDER_ALREADY_PAID
        elif self.order.type == OrderType.VIDEO_LESSON:
            if UserVideoLesson.objects.filter(
                video_lesson=self.order.video_lesson, user=self.order.user, order=self.order
            ).exists():
                self.error = True
                self.code = self.ORDER_ALREADY_PAID

    def validate_amount(self, amount):
        if amount != self.order.transaction_amount:
            self.error = True
            self.code = self.INVALID_AMOUNT
