from .base import *  # noqa

ALLOWED_HOSTS = [
    "lordstormrage.pythonanywhere.com", "127.0.0.1"
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEBUG = True

ADMINS = [("BlackHoler", "BilolMuhammadSolih@gmail.com")]
