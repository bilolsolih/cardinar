import requests
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from .choices import PART_TYPE, SUBCATEGORY
from phonenumber_field.modelfields import PhoneNumberField


class CustomProductModel(models.Model):
    category = models.CharField(max_length=1, choices=PART_TYPE)
    title = models.CharField(max_length=256, verbose_name=_('Product model'))
    photo = models.ImageField(upload_to='constructor/models/', verbose_name=_('Default photo'))

    class Meta:
        verbose_name = _('Custom product model')
        verbose_name_plural = _('Custom product models')

    def __str__(self):
        return self.title


class Part(models.Model):
    category = models.CharField(max_length=1, choices=PART_TYPE)
    subcategory = models.CharField(max_length=1, choices=SUBCATEGORY)
    product_model = models.ForeignKey('constructor.CustomProductModel', related_name='parts', on_delete=models.PROTECT,
                                      verbose_name=_('Product model'))
    title = models.CharField(max_length=256, verbose_name=_('Part name'), blank=True, null=True)
    material = models.ForeignKey('store.BuildingMaterial', related_name='parts', on_delete=models.PROTECT,
                                 verbose_name=_('Material'))
    color = models.ForeignKey('store.Color', related_name='parts', on_delete=models.PROTECT,
                              verbose_name=_('Color of the part'))
    photo = models.ImageField(upload_to='constructor/parts/', verbose_name=_('Photo of the part'))

    class Meta:
        verbose_name = _('Part')
        verbose_name_plural = _('Parts')

    def __str__(self):
        return f"{self.title} - {self.color.title}"


class CustomProduct(TimeStampedModel):
    category = models.CharField(max_length=1, choices=PART_TYPE)
    product = models.ForeignKey('store.Product', related_name='custom_products', on_delete=models.SET_NULL, null=True, verbose_name=_('Product'))
    product_model = models.ForeignKey('constructor.CustomProductModel', related_name='products', on_delete=models.PROTECT, verbose_name=_('Product model'))
    full_name = models.CharField(_('Full name'), max_length=128)
    phone_number = PhoneNumberField(_('Phone number'))
    email = models.EmailField(_('Email'), blank=True, null=True)
    photo = models.ImageField(_('Constructed product photo'), upload_to='images/constructor/products/%Y/%m/')
    car_model = models.ForeignKey('store.CarModel', related_name='custom_products', on_delete=models.CASCADE, verbose_name=_('Car model'), null=True, blank=True)

    remove_logo = models.BooleanField(default=False, verbose_name=_('Remove the logo?'))
    remove_podpyatnik = models.BooleanField(default=False, verbose_name=_('Remove the podpyatnik'), blank=True, null=True)

    is_active = models.BooleanField(_('Active status'), default=True)

    class Meta:
        verbose_name = _('Custom product')
        verbose_name_plural = _('Custom products')

    def __str__(self):
        return f"Custom product - {self.product_model.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        telegram_bot_token = '6689575443:AAHn148ymq6VL8qVgsLsv-iVVWfLoGOCi4Q'
        chat_id = '-1001915286015'

        message = f"Full Name: {self.full_name}\n"
        message += f"Phone Number: {self.phone_number}\n"
        message += f"Email: {self.email}\n"
        message += f"Марка Автомобиля: {self.product.car_brands}\n"

        files = {'photo': open(self.photo.path, 'rb')}

        response = requests.post(
            f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto",
            data={'chat_id': chat_id, 'caption': message},
            files=files
        )

        if response.status_code != 200:
            pass
