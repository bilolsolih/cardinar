from .base import *  # noqa

ALLOWED_HOSTS = ["cardinar.uz", "www.cardinar.uz", '127.0.0.1']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEBUG = True

ADMINS = [("BlackHoler", "BilolMuhammadSolih@gmail.com")]
