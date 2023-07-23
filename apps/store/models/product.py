import os

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from apps.store.choices import PRODUCT_STATUS, PRODUCT_TYPE


class BaseProduct(models.Model):
    category = models.ForeignKey(
        verbose_name=_('Category'), to='store.Category', related_name='%(class)ss', on_delete=models.SET_NULL, null=True
    )
    main_color = models.ForeignKey(
        verbose_name=_('Main color'), to='store.Color', related_name='%(class)ss', on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(verbose_name=_('Title'), max_length=256)
    type = models.CharField(verbose_name=_('Type'), choices=PRODUCT_TYPE, max_length=1, default='b')
    status = models.CharField(verbose_name=_('Status'), choices=PRODUCT_STATUS, max_length=1, default='n')
    photo = models.ImageField(verbose_name=_('Photo'), upload_to='images/store/products/%(class)ss/%Y/%m/%d')
    description = models.TextField(verbose_name=_('Description'))
    price = models.DecimalField(verbose_name=_('Price'), max_digits=24, decimal_places=2)
    purchase_count = models.PositiveIntegerField(verbose_name=_('Purchase count'), default=0)
    is_constructed = models.BooleanField(verbose_name=_('Is constructed?'), default=False)
    car_brands = models.ManyToManyField(verbose_name=_('Car brands'), to='store.CarBrand', related_name='%(class)ss')
    car_models = models.ManyToManyField(verbose_name=_('Car models'), to='store.CarModel', related_name='%(class)ss')
    active = models.BooleanField(verbose_name=_('Is active'), default=True)

    created = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True, null=True)
    updated = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True, null=True)

    class Meta:
        abstract = True


# TODO: sotib olinganida purchase_count increment qilinishi kerak
class CarCover(BaseProduct):
    central_part_color = models.ForeignKey(
        verbose_name=_('Central part color'), to='store.Color', related_name='%(class)ss', on_delete=models.SET_NULL, null=True
    )
    central_part_material = models.ForeignKey(
        verbose_name=_('Central material'), to='store.BuildingMaterial', related_name='%(class)ss', on_delete=models.SET_NULL, null=True
    )
    rear_color = models.ForeignKey(
        verbose_name=_('Rear color'), to='store.Color', related_name='%(class)ss', on_delete=models.SET_NULL, null=True
    )
    rear_material = models.ForeignKey(
        verbose_name=_('Rear material'), to='store.BuildingMaterial', related_name='%(class)ss', on_delete=models.SET_NULL, null=True
    )
    side_color = models.ForeignKey(
        verbose_name=_('Side color'), to='store.Color', related_name='%(class)ss', on_delete=models.SET_NULL, null=True
    )
    side_material = models.ForeignKey(
        verbose_name=_('Side material'), to='store.BuildingMaterial', related_name='%(class)ss', on_delete=models.SET_NULL, null=True
    )
    stitch_color = models.ForeignKey(
        verbose_name=_('Stitch color'), to='store.Color', related_name='%(class)ss', on_delete=models.SET_NULL, null=True
    )
    has_kant = models.BooleanField(
        verbose_name=_('Has Kant?'), default=True
    )
    kant_color = models.ForeignKey(
        verbose_name=_('Kant color'), to='store.Color', related_name='%(class)ss', on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = _('Car cover')
        verbose_name_plural = _('Car covers')

    def __str__(self):
        return f"{self.title} - {self.category.title}"


class Polik(BaseProduct):
    class Meta:
        verbose_name = _('Polik')
        verbose_name_plural = _('Poliks')

    def __str__(self):
        return f"{self.title} - {self.category.title}"


class Nakidka(BaseProduct):
    class Meta:
        verbose_name = _('Nakidka')
        verbose_name_plural = _('Nakidkas')

    def __str__(self):
        return f"{self.title} - {self.category.title}"


# TODO: similar products ni aniqlash uchun algo va API

class Category(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=128)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class Photo(TimeStampedModel):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('carcover', 'polik', 'nakidka')}
    )
    object_id = models.PositiveIntegerField(verbose_name=_('Object id'))
    product = GenericForeignKey('content_type', 'object_id')
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
