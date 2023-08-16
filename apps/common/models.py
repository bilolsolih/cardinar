from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True, null=True)
    updated = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True, null=True)

    class Meta:
        abstract = True
