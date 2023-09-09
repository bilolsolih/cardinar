from .base import *  # noqa
from os import getenv

ALLOWED_HOSTS = ['bilolsolih.pythonanywhere.com', 'api.cardinar.uz']

DATABASES = {
    "default": {
        "ENGINE": getenv('DB_ENGINE'),
        "NAME": getenv('DB_NAME'),
        "USER": getenv('DB_USER'),
        "PASSWORD": getenv('DB_PASSWORD'),
        "HOST": getenv('DB_HOST'),
        "PORT": getenv('DB_PORT')
    }
}

DEBUG = True

ADMINS = [("BlackHoler", "BilolMuhammadSolih@gmail.com")]