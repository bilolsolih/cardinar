from .base import *  # noqa

ALLOWED_HOSTS = ['bilolsolih.pythonanywhere.com', 'api.cardinar.uz', '127.0.0.1']
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "ATOMIC": False,
    }
}

DEBUG = True

ADMINS = [("BlackHoler", "BilolMuhammadSolih@gmail.com")]
