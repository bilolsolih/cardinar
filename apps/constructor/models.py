from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel


class ConstructedProduct(TimeStampedModel):
    category = models.ForeignKey(
        verbose_name=_('Category'), to='store.Category', related_name='constructed_products', on_delete=models.SET_NULL, null=True
    )
    photo = models.ImageField(verbose_name=_('Photo'), upload_to='images/store/products/%Y/%m/%d')
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
    edge_color = models.ForeignKey(
        verbose_name=_('Edge color'), to='store.Color', related_name='rc_products', on_delete=models.SET_NULL, null=True, blank=True
    )
    edge_material = models.ForeignKey(
        verbose_name=_('Edge material'), to='store.BuildingMaterial', related_name='rm_products', on_delete=models.SET_NULL, null=True, blank=True
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
        verbose_name = _('Constructed Product')
        verbose_name_plural = _('Constructed Products')

    def __str__(self):
        return f"{self.title} - {self.category.title}"
