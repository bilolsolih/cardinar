from io import BytesIO
from time import sleep

from PIL import Image
from celery import shared_task
from django.apps import apps
from django.core.files.base import ContentFile


@shared_task
def photo_compress(pk, app_label, model_name, side=1920):
    model = apps.get_model(app_label=app_label, model_name=model_name)
    instance = model.objects.filter(pk=pk).first()
    while not instance:
        sleep(1)
        instance = model.objects.filter(pk=pk).first()
    photo_width = instance.photo.width
    photo_height = instance.photo.height
    if photo_width > side or photo_height > side:
        if photo_width >= photo_height:
            width = side
            height = int(photo_height // (photo_width / width))
        else:
            height = side
            width = int(photo_width // (photo_height / height))
        buffer = BytesIO()
        quality = 80 if instance.status != 'Hit' or side > 1920 else 100
        resized_image = Image.open(instance.photo.path).resize(size=(width, height))
        if resized_image.mode != 'RGBA':
            resized_image = resized_image.convert('RGBA')
        resized_image.save(fp=buffer, format='PNG', quality=quality, optimize=True)
        file_name = f"compressed_{instance.photo.name.rsplit('/', 1)[-1]}.png"
        instance.photo.delete()
        instance.photo.save(file_name, ContentFile(buffer.getvalue()))
        instance.save()
    else:
        pass
