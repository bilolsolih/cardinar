import os

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
    category = models.ForeignKey(
        verbose_name=_('Category'), to='store.Category', related_name='products', on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(verbose_name=_('Title'), max_length=256)
    type = models.CharField(verbose_name=_('Type'), choices=PRODUCT_TYPE, max_length=7, default='Basic')
    status = models.CharField(verbose_name=_('Status'), choices=PRODUCT_STATUS, max_length=4, blank=True, null=True)
    photo = models.ImageField(verbose_name=_('Photo'), upload_to='images/store/products/%Y/%m/%d')
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name=_('Price'))
    no_in_stock = models.PositiveIntegerField(verbose_name=_('Number in stock'), null=True, blank=True)
    purchase_count = models.PositiveIntegerField(verbose_name=_('Purchase count'), default=0)
    is_constructed = models.BooleanField(verbose_name=_('Is constructed?'), default=False)
    car_brands = models.ManyToManyField(verbose_name=_('Car brands'), to='store.CarBrand', related_name='products', blank=True)
    car_models = models.ManyToManyField(verbose_name=_('Car models'), to='store.CarModel', related_name='products')
    main_color = models.ForeignKey(verbose_name=_('Main color'), to='store.Color', related_name='mc_products', on_delete=models.SET_NULL, null=True)
    building_material = models.ForeignKey(
        verbose_name=_('Building material'), to='store.BuildingMaterial', related_name='bm_products', on_delete=models.SET_NULL, null=True
    )
    central_part_color = models.ForeignKey(
        verbose_name=_('Central part color'), to='store.Color', related_name='cp_products', on_delete=models.SET_NULL, null=True, blank=True
    )
    central_part_material = models.ForeignKey(
        verbose_name=_('Central material'), to='store.BuildingMaterial', related_name='cp_products', on_delete=models.SET_NULL, null=True, blank=True
    )
    rear_color = models.ForeignKey(
        verbose_name=_('Rear color'), to='store.Color', related_name='rc_products', on_delete=models.SET_NULL, null=True, blank=True
    )
    rear_material = models.ForeignKey(
        verbose_name=_('Rear material'), to='store.BuildingMaterial', related_name='rm_products', on_delete=models.SET_NULL, null=True, blank=True
    )
    side_color = models.ForeignKey(
        verbose_name=_('Side color'), to='store.Color', related_name='sc_products', on_delete=models.SET_NULL, null=True, blank=True
    )
    side_material = models.ForeignKey(
        verbose_name=_('Side material'), to='store.BuildingMaterial', related_name='sm_products', on_delete=models.SET_NULL, null=True, blank=True
    )
    stitch_color = models.ForeignKey(
        verbose_name=_('Stitch color'), to='store.Color', related_name='st_products', on_delete=models.SET_NULL, null=True, blank=True
    )
    has_kant = models.BooleanField(
        verbose_name=_('Has Kant?'), default=False
    )
    kant_color = models.ForeignKey(
        verbose_name=_('Kant color'), to='store.Color', related_name='k_products', on_delete=models.SET_NULL, null=True, blank=True
    )

    active = models.BooleanField(verbose_name=_('Is active'), default=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Product')

    def __str__(self):
        return f"{self.title} - {self.category.title}"


# TODO: sotib olinganida purchase_count increment qilinishi kerak
# TODO: chexol uchun modell chexla qo'shish - model orqali
# TODO: similar products ni aniqlash uchun algo va API


class Photo(TimeStampedModel):
    product = models.ForeignKey(verbose_name=_('Product'), to='store.Product', related_name='photos', on_delete=models.PROTECT)
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

# TODO: kerakli modellarning barchasi adminga qo'shilganini tekshirish
