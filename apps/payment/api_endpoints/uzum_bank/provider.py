from django.utils.translation import gettext_lazy as _

from apps.course.models import UserCourse, UserVideoLesson
from apps.payment.models import (
    Order,
    OrderType,
    PaymentType,
    Transaction,
    TransactionStatus,
)
from apps.webinar.models import UserWebinar


class ApelsinProvider:
    def __init__(self, order_id):
        self.order_id = order_id
        self.order = self.get_order()
        self.error = None
        self.error_message = None

    def pay_info(self, transaction_id, amount):
        if not self.order:
            return True, _("Order does not exist"), self.order

        Transaction.objects.get_or_create(
            transaction_id=transaction_id,
            order=self.order,
            defaults={"amount": amount, "status": TransactionStatus.WAITING},
        )

        self.validate_order()
        self.validate_amount(amount)
        return self.error, self.error_message, self.order

    def validate_amount(self, amount):
        if amount != self.order.transaction_amount:
            self.error = True
            self.error_message = _("Invalid amount")

    def get_order_info(self):
        if not self.order:
            return True, _("Order does not exist"), self.order

        # validate order
        self.validate_order()

        return self.error, self.error_message, self.order

    def validate_order(self):
        if self.order.is_paid:
            self.error = True
            self.error_message = _("Order is already paid")
        if self.order.payment_type != PaymentType.ONE_TIME:
            self.error = True
            self.error_message = _("Invalid payment type")
        self.validate_order_type()

    def get_order(self):
        try:
            return Order.objects.get(id=self.order_id)
        except Order.DoesNotExist:
            return

    def validate_order_type(self):
        if self.order.type == OrderType.COURSE:
            if UserCourse.objects.filter(course=self.order.course, user=self.order.user, order=self.order).exists():
                self.error = True
                self.error_message = _("You have already bought this course")
        elif self.order.type == OrderType.WEBINAR:
            if UserWebinar.objects.filter(webinar=self.order.webinar, user=self.order.user, order=self.order).exists():
                self.error = True
                self.error_message = _("You have already bought this webinar")
        elif self.order.type == OrderType.VIDEO_LESSON:
            if UserVideoLesson.objects.filter(
                video_lesson=self.order.video_lesson, user=self.order.user, order=self.order
            ).exists():
                self.error = True
                self.error_message = _("You have already bought this video lesson")
