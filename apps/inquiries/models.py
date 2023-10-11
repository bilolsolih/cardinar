from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedModel


class Inquiry(TimeStampedModel):
    full_name = models.CharField(verbose_name=_('Full name'), max_length=128)
    phone_number = PhoneNumberField(verbose_name=_('Phone number'))
    email = models.CharField(verbose_name=_('Email'), blank=True, null=True, max_length=256)
    comment = models.TextField(verbose_name=_('Comment'), blank=True, null=True)
    on_product = models.ForeignKey(
        verbose_name=_('On product'), to='store.Product', related_name='inquiries', on_delete=models.CASCADE, blank=True, null=True
    )
    articul = models.ForeignKey('store.Articul', related_name='inquiries', on_delete=models.SET_NULL, null=True, blank=True)
    is_one_click = models.BooleanField(default=False)
    is_call = models.BooleanField(default=False)
    is_product = models.BooleanField(default=True)

    active = models.BooleanField(verbose_name=_('Active?'), default=True)

    class Meta:
        verbose_name = _('Inquiry on product')
        verbose_name_plural = _('Inquiries on product')

    def __str__(self):
        return f"Inquiry by {self.full_name} - {self.phone_number}"


class InquiryCall(Inquiry):
    class Meta:
        proxy = True
        verbose_name = _('Inquiry for call')
        verbose_name_plural = _('Inquiries for call')


class InquiryOneClick(Inquiry):
    class Meta:
        proxy = True
        verbose_name = _('Inquiry for One-click-buy')
        verbose_name_plural = _('Inquiries for One-click-buy')
