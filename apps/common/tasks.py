from io import BytesIO
from time import sleep

from PIL import Image
from celery import shared_task
from django.apps import apps
from django.core.files.base import ContentFile


@shared_task
def photo_compress(pk, app_label, model_name, side=1024):
    model = apps.get_model(app_label=app_label, model_name=model_name)
    instance = model.objects.filter(pk=pk).first()
    while not instance:
        sleep(1)
        instance = model.objects.filter(pk=pk).first()

    photo_height = instance.photo.height
    photo_width = instance.photo.width

    if photo_height > side:
        height = side
        width = int(photo_width / (photo_height / height))
        buffer = BytesIO()
        quality = 100
        resized_image = Image.open(instance.photo.path).resize(size=(width, height))
        resized_image.save(fp=buffer, format='PNG', quality=quality, optimize=True)
        file_name = f"compressed_{instance.photo.name.rsplit('/', 1)[-1]}"
        instance.photo.delete()
        instance.photo.save(file_name, ContentFile(buffer.getvalue()))
        instance.save()
