from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import PART_TYPE


class Part(models.Model):
    category = models.CharField(max_length=1, choices=PART_TYPE)
    title = models.CharField(max_length=256, verbose_name=_('Part name'))
    color_title = models.CharField(max_length=64, verbose_name=_('Color name'))
    hex = models.CharField(max_length=24, verbose_name=_('Color hex value'))
    photo = models.ImageField(upload_to='constructor/parts/', verbose_name=_('Photo of the part'))

    class Meta:
        verbose_name = _('Part')
        verbose_name_plural = _('Parts')

    def __str__(self):
        return f"{self.title} - {self.color_title}"
