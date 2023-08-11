import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.develop')

celery_app = Celery('cardinar')
celery_app.config_from_object(settings)
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
