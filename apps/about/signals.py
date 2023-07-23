from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common.tasks import photo_compress
from .models import Banner


@receiver(signal=post_save, sender=Banner)
def banner_post_save(sender, instance, created, **kwargs):
    if created and instance.photo and instance.photo.width > 1920:
        photo_compress.delay(pk=instance.pk, app_label=instance._meta.app_label, model_name=instance._meta.model_name, quality=85)
