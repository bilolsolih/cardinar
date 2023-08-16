from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
import os

from apps.common.models import TimeStampedModel


class Banner(TimeStampedModel):
    photo = models.ImageField(verbose_name=_('Photo'), upload_to='images/about/banners/')
    text = models.TextField(verbose_name=_('Text'), blank=True, null=True)

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    def delete(self, *args, **kwargs):
        if self.photo and os.path.exists(self.photo.path):
            os.remove(self.photo.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Banner {self.id}"


class PhoneNumber(models.Model):
    phone_number = PhoneNumberField(verbose_name=_('Phone number'), unique=True)

    class Meta:
        verbose_name = _('Phone number')
        verbose_name_plural = _('Phone numbers')

    def __str__(self):
        return self.phone_number.__str__()


class Email(models.Model):
    email = models.EmailField(verbose_name=_('Email'), unique=True)

    class Meta:
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')

    def __str__(self):
        return self.email


class Address(models.Model):
    region = models.CharField(verbose_name=_('Region'), max_length=128)
    district = models.CharField(verbose_name=_('District'), max_length=128)
    street = models.CharField(verbose_name=_('Street'), max_length=128)
    house_no = models.PositiveIntegerField(verbose_name=_('House number'), null=True, blank=True)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f"{self.region}, {self.district}, {self.street}, {self.house_no}"


class SocialMedia(models.Model):
    social_media = models.CharField(verbose_name=_('Social Media'), max_length=128)
    link = models.URLField(verbose_name=_('Link'))

    class Meta:
        verbose_name = _('Social Media')
        verbose_name_plural = _('Social Medias')
        unique_together = ['social_media', 'link']

    def __str__(self):
        return f"{self.social_media} - {self.link}"

# TODO: Gde Kupit, Footerda, hal qilish kerak
# TODO: barcha kerakli modellarni translation admin bilan register qilib chiqish kerak
