import base64

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedModel
from .choices import DELIVERY_TYPES, ORDER_STATUS, PAYMENT_STATUS


class Order(models.Model):
    user = models.ForeignKey('users.User', related_name='orders', on_delete=models.CASCADE, blank=True, null=True,
                             verbose_name=_('User'))
    store = models.ForeignKey('store.Store', related_name='orders', on_delete=models.SET_NULL, null=True,
                              verbose_name=_('Store'))
    full_name = models.CharField(_('Full name'), max_length=128)
    phone_number = PhoneNumberField(_('Phone number'), region='UZ')
    email = models.EmailField(_('Email'), blank=True, null=True)
    delivery_type = models.CharField(_('Delivery type'), choices=DELIVERY_TYPES, max_length=1)

    is_paid = models.BooleanField(default=False, verbose_name=_("Is Paid"))
    is_canceled = models.BooleanField(default=False, verbose_name=_("Is Canceled"))

    status = models.CharField(verbose_name=_('Status'), max_length=1, choices=ORDER_STATUS, default='p')
    payment_status = models.CharField(_('Payment status'), max_length=2, choices=PAYMENT_STATUS, default='wp')

    created = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    @property
    def get_title(self):
        return ', '.join([item.product.title for item in self.items.all()])

    @property
    def final_price(self):
        return self.items.aggregate(final_price=models.Sum('cost'))['final_price']

    def get_payment_url(self):
        merchant_id = settings.PROVIDERS["payme"]["merchant_id"]
        params = f"m={merchant_id};ac.order_id={self.id};a={self.final_price * 100};c=https://cardinar.uz"
        encode_params = base64.b64encode(params.encode("utf-8"))
        encode_params = str(encode_params, "utf-8")
        payment_url = f"{settings.PROVIDERS['payme']['callback_url']}/{encode_params}"
        return payment_url

    def __str__(self):
        if self.user:
            return f"Order {self.id} by {self.user.username}"
        else:
            return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(verbose_name=_('Order'), to='orders.Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name=_('Product'), to='store.Product', related_name='order_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    cost = models.PositiveIntegerField(verbose_name=_('Cost'), blank=True, null=True)
    car_model = models.ForeignKey(verbose_name=_('Car model'), to='store.CarModel', related_name='order_items', on_delete=models.CASCADE)

    @property
    def get_product_title(self):
        return self.product.title

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
        return f"{self.get_product_title} - {self.quantity} - {self.cost}"


class PaymentType(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=128)

    class Meta:
        verbose_name = _('Payment type')
        verbose_name_plural = _('Payment types')

    def __str__(self):
        return self.title

# todo: api lardagi permissionlarni ko'rib chiqish
