from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common.tasks import photo_compress
from .models import Banner


@receiver(signal=post_save, sender=Banner)
def banner_post_save(sender, instance, created, **kwargs):
    if created and instance.photo:
        photo_compress(pk=instance.pk, app_label=instance._meta.app_label, model_name=instance._meta.model_name, side=1920)
