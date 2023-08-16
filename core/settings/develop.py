from .base import *  # noqa


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "ATOMIC": False,
    }
}

DEBUG = True

ALLOWED_HOSTS = ["cardinar.uz", "www.cardinar.uz"]
