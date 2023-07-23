from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .choices import DELIVERY_TYPES, ORDER_STATUS


class Order(models.Model):
    user = models.ForeignKey(
        verbose_name=_('User'), to='users.User', related_name='orders', on_delete=models.CASCADE, null=True
    )
    store = models.ForeignKey(
        verbose_name=_('Store'), to='store.Store', related_name='orders', on_delete=models.SET_NULL, null=True
    )
    full_name = models.CharField(verbose_name=_('Full name'), max_length=128)
    phone_number = PhoneNumberField(verbose_name=_('Phone number'), region='UZ')
    email = models.EmailField(verbose_name=_('Email'), blank=True, null=True)
    delivery_type = models.CharField(verbose_name=_('Delivery type'), choices=DELIVERY_TYPES, max_length=1)
    payment_method = models.ForeignKey(
        verbose_name=_('Payment method'), to='orders.PaymentType', related_name='orders', on_delete=models.SET_NULL, null=True
    )
    final_price = models.DecimalField(verbose_name=_('Final price'), max_digits=24, decimal_places=2, default=0)
    created = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    status = models.CharField(verbose_name=_('Status'), max_length=1, choices=ORDER_STATUS, default='p')

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        verbose_name=_('Order'), to='orders.Order', related_name='items', on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('carcover', 'polik', 'nakidka')}
    )
    object_id = models.PositiveIntegerField(verbose_name=_('Object id'))
    product = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    cost = models.DecimalField(verbose_name=_('Cost'), max_digits=24, decimal_places=2)

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
