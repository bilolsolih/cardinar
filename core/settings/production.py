from .base import *  # noqa

ALLOWED_HOSTS = [
    "http://lordstormrage.pythonanywhere.com",
    "https://lordstormrage.pythonanywhere.com",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEBUG = False

ADMINS = [("BlackHoler", "BilolMuhammadSolih@gmail.com")]
