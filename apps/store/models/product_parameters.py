from django.db import models
from django.utils.translation import gettext_lazy as _


class BuildingMaterial(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=128)

    class Meta:
        verbose_name = _('Material')
        verbose_name_plural = _('Materials')

    def __str__(self):
        return self.title


class CarBrand(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=128, unique=True)

    class Meta:
        verbose_name = _('Car brand')
        verbose_name_plural = _('Car brands')

    def __str__(self):
        return self.title


class CarModel(models.Model):
    brand = models.ForeignKey(verbose_name=_('Car brands'), to='store.CarBrand', related_name='cars', on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('Title'), max_length=128)

    class Meta:
        verbose_name = _('Car model')
        verbose_name_plural = _('Car models')
        # unique_together = ['brand', 'title']

    def __str__(self):
        return f"{self.brand.title} - {self.title}"


class Color(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=128)
    hex_value = models.CharField(verbose_name=_('Hex value'), max_length=24)

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')

    def __str__(self):
        return f"{self.title} - {self.hex_value}"
