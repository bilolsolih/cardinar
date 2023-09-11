from .base import *  # noqa
from os import getenv

ALLOWED_HOSTS = ['bilolsolih.pythonanywhere.com', 'api.cardinar.uz', '127.0.0.1']
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "ATOMIC": False,
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": getenv('DB_ENGINE'),
#         "NAME": getenv('DB_NAME'),
#         "USER": getenv('DB_USER'),
#         "PASSWORD": getenv('DB_PASSWORD'),
#         "HOST": getenv('DB_HOST'),
#         "PORT": getenv('DB_PORT')
#     }
# }

DEBUG = True

ADMINS = [("BlackHoler", "BilolMuhammadSolih@gmail.com")]