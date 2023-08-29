from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Store(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=128)
    phone_number = PhoneNumberField(verbose_name=_('Phone number'), region='UZ')
    is_official = models.BooleanField(verbose_name=_('Is official?'), default=True)
    region = models.CharField(verbose_name=_('Region'), max_length=128)
    district = models.CharField(verbose_name=_('City or district'), max_length=128)
    address = models.CharField(verbose_name=_('Address'), max_length=256)
    orient = models.CharField(verbose_name=_('Orient'), max_length=256)

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return f"{self.title} in {self.region}, {self.district}"
