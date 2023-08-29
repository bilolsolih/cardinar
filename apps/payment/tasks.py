from celery import shared_task

from django.utils import timezone

from apps.payment.api_endpoints.card.service import KarmonPayClient
from apps.payment.models import (
    InstallmentLog,
    InstallmentLogStatus,
    Order,
    PaymentType,
    Provider,
    TransactionStatus,
)


def pay(order):
    error, response, transaction = KarmonPayClient().pay(order)
    if error:
        InstallmentLog.objects.create(
            order=order, transaction=transaction, detail=response, status=InstallmentLogStatus.FAILED
        )
        if transaction:
            transaction.status = TransactionStatus.FAILED
            transaction.save()
        return

    transaction.apply()
    InstallmentLog.objects.create(
        order=order, transaction=transaction, detail=response, status=InstallmentLogStatus.SUCCESS
    )


@shared_task(time_limit=7200)
def installment_executor():
    orders = Order.objects.filter(
        is_paid=False,
        provider=Provider.CARD,
        payment_type__in=[PaymentType.TWO_TIME, PaymentType.FOUR_TIME],
        transaction__isnull=False,
        transaction__status=TransactionStatus.PAID,
    ).distinct()
    for order in orders:
        success_transactions = order.transaction_set.filter(status=TransactionStatus.PAID).order_by("paid_at")
        success_transactions_count = success_transactions.count()
        first_success_transaction = success_transactions.first()

        if success_transactions_count == 1 and (
            timezone.now() - first_success_transaction.paid_at > timezone.timedelta(days=30)
        ):
            pay(order)
        elif success_transactions_count == 2 and (
            timezone.now() - first_success_transaction.paid_at > timezone.timedelta(days=60)
        ):
            pay(order)
        elif success_transactions_count == 3 and (
            timezone.now() - first_success_transaction.paid_at > timezone.timedelta(days=90)
        ):
            pay(order)
        elif success_transactions_count == 4 and (
            timezone.now() - first_success_transaction.paid_at > timezone.timedelta(days=120)
        ):
            pay(order)
