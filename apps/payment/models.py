from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel


class TransactionStatus(models.TextChoices):
    WAITING = "waiting", _("Waiting")
    PAID = "paid", _("Paid")
    FAILED = "failed", _("Failed")
    CANCELED = "canceled", _("Canceled")


class InstallmentLogStatus(models.TextChoices):
    FAILED = "failed", _("Failed")
    SUCCESS = "success", _("Success")


class Transaction(TimeStampedModel):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    transaction_id = models.CharField(max_length=255, null=True, verbose_name=_("Transaction ID"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    status = models.CharField(max_length=63, verbose_name=_("Status"), choices=TransactionStatus.choices)
    paid_at = models.DateTimeField(verbose_name=_("Paid At"), null=True, blank=True)
    cancel_time = models.DateTimeField(verbose_name=_("Cancel Time"), null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.transaction_id}"

    def apply(self):
        self.status = TransactionStatus.PAID
        self.paid_at = timezone.now()
        self.save()
        self.apply_order()

    def apply_order(self):
        self.order.is_paid = True
        self.order.save()

    def cancel(self):
        self.status = TransactionStatus.CANCELED
        self.cancel_time = timezone.now()
        self.save()
        self.order.is_paid = False
        self.order.is_canceled = True
        self.order.save()

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")


class PaymentMerchantRequestLog(TimeStampedModel):
    header = models.TextField(verbose_name=_("Header"))
    body = models.TextField(verbose_name=_("Body"))
    method = models.CharField(verbose_name=_("Method"), max_length=32)
    response = models.TextField(null=True, blank=True)
    response_status_code = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=32)

    class Meta:
        verbose_name = _("Payment Merchant Request Log")
        verbose_name_plural = _("Payment Merchant Request Logs")


class InstallmentLog(TimeStampedModel):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    transaction = models.ForeignKey("payment.Transaction", on_delete=models.CASCADE, verbose_name=_("Transaction"), null=True)
    detail = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=63, verbose_name=_("Status"), choices=InstallmentLogStatus.choices)

    class Meta:
        verbose_name = _("Installment Log")
        verbose_name_plural = _("Installment Logs")
