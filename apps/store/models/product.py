import os

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from apps.store.choices import PRODUCT_STATUS, PRODUCT_TYPE


class Category(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=128)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class Product(TimeStampedModel):
    category = models.ForeignKey(verbose_name=_('Category'), to='store.Category', related_name='products',
                                 on_delete=models.PROTECT)
    title = models.CharField(verbose_name=_('Title'), max_length=256)
    type = models.CharField(verbose_name=_('Type'), choices=PRODUCT_TYPE, max_length=7, default='Basic')
    status = models.CharField(verbose_name=_('Status'), choices=PRODUCT_STATUS, max_length=4, blank=True, null=True)
    photo = models.ImageField(verbose_name=_('Photo'), upload_to='images/store/products/%Y/%m/%d')
    description = RichTextField(verbose_name=_('Description'), blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name=_('Price'))
    no_in_stock = models.PositiveIntegerField(verbose_name=_('Number in stock'), null=True, blank=True)
    purchase_count = models.PositiveIntegerField(verbose_name=_('Purchase count'), default=0)
    car_brands = models.ManyToManyField(verbose_name=_('Car brands'), to='store.CarBrand', related_name='products',
                                        blank=True)
    car_models = models.ManyToManyField(verbose_name=_('Car models'), to='store.CarModel', related_name='products')
    main_color = models.ForeignKey(verbose_name=_('Main color'), to='store.Color', related_name='mc_products',
                                   on_delete=models.SET_NULL, null=True)
    building_material = models.ForeignKey(verbose_name=_('Building material'), to='store.BuildingMaterial',
                                          related_name='bm_products', on_delete=models.SET_NULL, null=True)

    is_constructable = models.BooleanField(_('Constructable status'), default=False)

    active = models.BooleanField(verbose_name=_('Is active'), default=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Product')

    @property
    def category_title(self):
        return self.category.title

    def __str__(self):
        return f"{self.title} - {self.category.title}"


class Articul(models.Model):
    product = models.ForeignKey('store.Product', related_name='articuls', on_delete=models.CASCADE)
    car_model = models.ForeignKey('store.CarModel', related_name='articuls', on_delete=models.PROTECT)
    title = models.CharField(max_length=128)

    class Meta:
        verbose_name = _('Articul')
        verbose_name_plural = _('Articuls')

    def __str__(self):
        return f"{self.title} - {self.product}"


class Photo(TimeStampedModel):
    product = models.ForeignKey(verbose_name=_('Product'), to='store.Product', related_name='photos',
                                on_delete=models.PROTECT)
    title = models.CharField(verbose_name=_('Title'), max_length=256)
    photo = models.ImageField(verbose_name=_('Photo'), upload_to='images/store/products/%Y/%m/%d')

    class Meta:
        verbose_name = _('Product photo')
        verbose_name_plural = _('Product photos')

    def delete(self, *args, **kwargs):
        if self.photo.path and os.path.exists(self.photo.path):
            os.remove(self.photo.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


class PremiumPhoto(models.Model):
    product = models.ForeignKey('store.Product', related_name='images', on_delete=models.CASCADE)
    photo = models.ImageField(_('Photo'), upload_to='images/store/products/premium_photos/%Y/%m/')
    ordinal_number = models.PositiveIntegerField(_('Ordinal number'))

    class Meta:
        verbose_name = _('Premium photo')
        verbose_name_plural = _('Premium photos')
        ordering = ['ordinal_number']

    def __str__(self):
        return f'Premium photo for {self.product}'
