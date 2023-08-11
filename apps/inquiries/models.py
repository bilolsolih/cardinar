from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedModel


class Inquiry(TimeStampedModel):
    full_name = models.CharField(verbose_name=_('Full name'), max_length=128)
    phone_number = PhoneNumberField(verbose_name=_('Phone number'))
    email = models.EmailField(verbose_name=_('Email'), blank=True, null=True)
    on_product = models.ForeignKey(
        verbose_name=_('about product'), to='store.Product', related_name='inquires', on_delete=models.CASCADE, blank=True, null=True
    )
    active = models.BooleanField(verbose_name=_('Active?'), default=True)

    class Meta:
        verbose_name = _('Inquiry')
        verbose_name_plural = _('Inquiries')

    def __str__(self):
        return f"Inquiry by {self.full_name} - {self.phone_number}"

# TODO: bot token olib qo'shib qo'yish kerak
