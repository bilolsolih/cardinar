from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from .choices import PART_TYPE, SUBCATEGORY


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
    product_model = models.ForeignKey(
        'constructor.CustomProductModel', related_name='parts', on_delete=models.PROTECT, verbose_name=_('Product model')
    )
    title = models.CharField(max_length=256, verbose_name=_('Part name'), blank=True, null=True)
    material = models.ForeignKey(
        'store.BuildingMaterial', related_name='parts', on_delete=models.PROTECT, verbose_name=_('Material')
    )
    color = models.ForeignKey(
        'store.Color', related_name='parts', on_delete=models.PROTECT, verbose_name=_('Color of the part')
    )
    photo = models.ImageField(upload_to='constructor/parts/', verbose_name=_('Photo of the part'))

    class Meta:
        verbose_name = _('Part')
        verbose_name_plural = _('Parts')

    def __str__(self):
        return f"{self.title} - {self.color.title}"


class CustomProduct(TimeStampedModel):
    category = models.CharField(max_length=1, choices=PART_TYPE)
    product_model = models.ForeignKey('constructor.CustomProductModel', related_name='products', on_delete=models.PROTECT, verbose_name=_('Product model'))
    central_part = models.ForeignKey('constructor.Part', related_name='cp_products', on_delete=models.PROTECT, verbose_name=_('Central part'))
    back_part = models.ForeignKey('constructor.Part', related_name='bp_products', on_delete=models.PROTECT, verbose_name=_('Back part'), blank=True, null=True)
    rear_part = models.ForeignKey('constructor.Part', related_name='rp_products', on_delete=models.PROTECT, verbose_name=_('Rear part'))
    stitch = models.ForeignKey('constructor.Part', related_name='s_products', on_delete=models.PROTECT, verbose_name=_('Stitch'), blank=True, null=True)
    kant = models.ForeignKey('constructor.Part', related_name='k_products', on_delete=models.PROTECT, verbose_name=_('Kant'))

    remove_logo = models.BooleanField(default=False, verbose_name=_('Remove the logo?'))
    remove_podpyatnik = models.BooleanField(default=False, verbose_name=_('Remove the podpyatnik'), blank=True, null=True)

    # central_material = models.ForeignKey('store.BuildingMaterial', related_name='cm_customproducts', on_delete=models.PROTECT, verbose_name=_('Material of central part'))
    # central_color = models.ForeignKey('store.Color', related_name='cm_customproducts', on_delete=models.PROTECT, verbose_name=_('Color of central part'))
    # back_material = models.ForeignKey('store.BuildingMaterial', related_name='bm_customproducts', on_delete=models.PROTECT, verbose_name=_('Material of back part'))
    # back_color = models.ForeignKey('store.Color', related_name='bm_customproducts', on_delete=models.PROTECT, verbose_name=_('Color of back part'))
    # rear_material = models.ForeignKey('store.BuildingMaterial', related_name='rm_customproducts', on_delete=models.PROTECT, verbose_name=_('Material of rear part'))
    # rear_color = models.ForeignKey('store.Color', related_name='rm_customproducts', on_delete=models.PROTECT, verbose_name=_('Color of rear part'))
    # stitch_color = models.ForeignKey('store.Color', related_name='s_customproducts', on_delete=models.PROTECT, verbose_name=_('Color of stitch'))
    # kant_color = models.ForeignKey('store.Color', related_name='k_customproducts', on_delete=models.PROTECT, verbose_name=_('Color of Kant'))

    class Meta:
        verbose_name = _('Custom product')
        verbose_name_plural = _('Custom products')

    def __str__(self):
        return f"Custom product - {self.product_model.title}"
