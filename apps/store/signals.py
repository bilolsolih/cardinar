from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common.tasks import photo_compress
from apps.store.models.product import Product


@receiver(post_save, sender=Product)
def news_or_picture_saved(sender, instance, created, **kwargs):
    if created and instance.photo and instance.photo.width > 1920:
        photo_compress(instance.pk, instance._meta.app_label, instance._meta.model_name)
