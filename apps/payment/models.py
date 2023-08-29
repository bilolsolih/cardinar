import base64

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from apps.course.models import UserCourse, UserVideoLesson
from apps.webinar.models import UserWebinar


class OrderType(models.TextChoices):
    COURSE = "course", _("Course")
    VIDEO_LESSON = "video_lesson", _("Video Lesson")
    WEBINAR = "webinar", _("Webinar")


class PaymentType(models.TextChoices):
    ONE_TIME = "one_time", _("One Time")
    TWO_TIME = "two_time", _("Two Time")
    FOUR_TIME = "four_time", _("Four Time")


class Provider(models.TextChoices):
    PAYME = "payme", _("Payme")
    CLICK = "click", _("Click")
    KARMON_PAY = "karmon_pay", _("Karmon Pay")
    UZUM_BANK = "uzum_bank", _("Uzum Bank")
    CARD = "card", _("Card")


class TransactionStatus(models.TextChoices):
    WAITING = "waiting", _("Waiting")
    PAID = "paid", _("Paid")
    FAILED = "failed", _("Failed")
    CANCELED = "canceled", _("Canceled")


class InstallmentLogStatus(models.TextChoices):
    FAILED = "failed", _("Failed")
    SUCCESS = "success", _("Success")


# Create your models here.
class Order(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("User"))
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        verbose_name=_("Course"),
        null=True,
        blank=True,
        related_name="orders",
    )
    webinar = models.ForeignKey(
        "webinar.Webinar",
        on_delete=models.CASCADE,
        verbose_name=_("Webinar"),
        null=True,
        blank=True,
        related_name="orders",
    )
    video_lesson = models.ForeignKey(
        "course.VideoLesson",
        on_delete=models.CASCADE,
        verbose_name=_("Video lesson"),
        null=True,
        blank=True,
        related_name="orders",
    )
    user_card = models.ForeignKey(
        "UserCard", on_delete=models.PROTECT, verbose_name=_("User card"), null=True, blank=True, related_name="orders"
    )
    promo_code = models.CharField(verbose_name=_("Promo code"), max_length=255, null=True, blank=True)
    type = models.CharField(max_length=63, verbose_name=_("Type"), choices=OrderType.choices)
    payment_type = models.CharField(max_length=63, verbose_name=_("Payment Type"), choices=PaymentType.choices)
    provider = models.CharField(max_length=63, verbose_name=_("Provider"), choices=Provider.choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"))
    is_paid = models.BooleanField(default=False, verbose_name=_("Is Paid"))
    is_canceled = models.BooleanField(default=False, verbose_name=_("Is Canceled"))

    def __str__(self):
        if self.type == OrderType.COURSE:
            return f"{self.user} - {self.course} - {self.id}"
        elif self.type == OrderType.VIDEO_LESSON:
            return f"{self.user} - {self.video_lesson} - {self.id}"
        elif self.type == OrderType.WEBINAR:
            return f"{self.user} - {self.webinar} - {self.id}"
        return f"{self.user} - {self.type} - {self.id}"

    @property
    def transaction_amount(self):
        if self.payment_type == PaymentType.ONE_TIME:
            return self.total_amount
        elif self.payment_type == PaymentType.TWO_TIME:
            return self.total_amount / 2
        elif self.payment_type == PaymentType.FOUR_TIME:
            return self.total_amount / 4
        return self.total_amount

    def get_payment_url(self):
        payment_url = ""
        if self.provider == Provider.PAYME:
            merchant_id = settings.PROVIDERS["payme"]["merchant_id"]
            params = f"m={merchant_id};ac.order_id={self.id};a={self.transaction_amount * 100};c=https://ayoluchun.uz"
            encode_params = base64.b64encode(params.encode("utf-8"))
            encode_params = str(encode_params, "utf-8")
            payment_url = f"{settings.PROVIDERS[self.provider]['callback_url']}/{encode_params}"
        elif self.provider == Provider.CLICK:
            merchant_id = settings.PROVIDERS[self.provider]["merchant_id"]
            service_id = settings.PROVIDERS[self.provider]["merchant_service_id"]
            params = (
                f"?service_id={service_id}&merchant_id={merchant_id}&"
                f"amount={self.transaction_amount}&transaction_param={self.id}&return_url=https://ayoluchun.uz"
            )
            payment_url = f'{settings.PROVIDERS[self.provider]["callback_url"]}/{params}'
        elif self.provider == Provider.KARMON_PAY:
            merchant_id = settings.PROVIDERS[self.provider]["merchant_id"]
            params = f"merchant_id={merchant_id}&amount={self.transaction_amount}&account.order_id={self.id}"
            encode_params = base64.b64encode(params.encode("utf-8"))
            encode_params = str(encode_params, "utf-8")
            payment_url = f"{settings.PROVIDERS[self.provider]['callback_url']}/{encode_params}"
        elif self.provider == Provider.UZUM_BANK:
            params = f"?serviceId={settings.PROVIDERS[self.provider]['service_id']}&client_id={self.id}"
            payment_url = f"{settings.PROVIDERS[self.provider]['callback_url']}{params}"
        elif self.provider == Provider.CARD:
            payment_url = "https://card.uz"
        return payment_url

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class Transaction(TimeStampedModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    transaction_id = models.CharField(max_length=255, verbose_name=_("Transaction ID"), null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    status = models.CharField(max_length=63, verbose_name=_("Status"), choices=TransactionStatus.choices)
    paid_at = models.DateTimeField(verbose_name=_("Paid At"), null=True, blank=True)
    cancel_time = models.DateTimeField(verbose_name=_("Cancel Time"), null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.transaction_id}"

    def apply(self):
        self.status = TransactionStatus.PAID
        self.paid_at = timezone.now()
        if self.order.type == OrderType.COURSE:
            UserCourse.objects.get_or_create(
                user=self.order.user, course=self.order.course, defaults={"order": self.order}
            )
        elif self.order.type == OrderType.VIDEO_LESSON:
            UserCourse.objects.get_or_create(user=self.order.user, course=self.order.course)
            UserVideoLesson.objects.get_or_create(
                user=self.order.user,
                video_lesson=self.order.video_lesson,
                course=self.order.course,
                defaults={"order": self.order},
            )
        elif self.order.type == OrderType.WEBINAR:
            UserWebinar.objects.get_or_create(
                user=self.order.user, webinar=self.order.webinar, defaults={"order": self.order}
            )
        self.save()
        self.apply_order()

    def apply_order(self):
        if self.order.provider != Provider.CARD or self.order.payment_type == PaymentType.ONE_TIME:
            self.order.is_paid = True
        else:
            if self.order.payment_type == PaymentType.TWO_TIME:
                if self.order.transaction_set.filter(status=TransactionStatus.PAID).count() == 2:
                    self.order.is_paid = True
            elif self.order.payment_type == PaymentType.FOUR_TIME:
                if self.order.transaction_set.filter(status=TransactionStatus.PAID).count() == 4:
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


class UserCard(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("User"))
    card_number = models.CharField(max_length=255, verbose_name=_("Card Number"))
    expire_date = models.CharField(max_length=255, verbose_name=_("Expire Date"))
    card_id = models.CharField(max_length=255, verbose_name=_("Card ID"))
    token = models.CharField(max_length=255, verbose_name=_("Token"), null=True)
    confirmed = models.BooleanField(default=False, verbose_name=_("Confirmed"))

    class Meta:
        verbose_name = _("User Card")
        verbose_name_plural = _("User Cards")
        unique_together = ("user", "card_number")


class PaymentMerchantRequestLog(TimeStampedModel):
    provider = models.CharField(max_length=63, verbose_name=_("Provider"), choices=Provider.choices)
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
    order = models.ForeignKey("Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    transaction = models.ForeignKey("Transaction", on_delete=models.CASCADE, verbose_name=_("Transaction"), null=True)
    detail = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=63, verbose_name=_("Status"), choices=InstallmentLogStatus.choices)

    class Meta:
        verbose_name = _("Installment Log")
        verbose_name_plural = _("Installment Logs")


class PromoCode(TimeStampedModel):
    code = models.CharField(max_length=255, verbose_name=_("Code"), unique=True)
    percent = models.PositiveSmallIntegerField(verbose_name=_("Percent"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE, verbose_name=_("Course"))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Promo Code")
        verbose_name_plural = _("Promo Codes")

    @property
    def is_active(self):
        return self.start_date <= timezone.now().astimezone().date() <= self.end_date

    @property
    def is_used(self):
        return hasattr(self, "usedpromocode")


class UsedPromoCode(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("User"))
    promo_code = models.OneToOneField("PromoCode", on_delete=models.CASCADE, verbose_name=_("Promo Code"))
    order = models.ForeignKey("Order", on_delete=models.CASCADE, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Used Promo Code")
        verbose_name_plural = _("Used Promo Codes")
        unique_together = ("user", "promo_code")

    def __str__(self):
        return f"{self.user} - {self.promo_code}"
