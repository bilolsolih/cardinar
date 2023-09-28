import os
from datetime import timedelta
from pathlib import Path

import django.middleware.csrf
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# from ..jazzmin import *  # noqa

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

# Application definition

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "ckeditor",
    'corsheaders',
    'rosetta',
    'phonenumber_field',
]

CUSTOM_APPS = [
    "apps.common",
    "apps.users",
    "apps.about",
    "apps.store",
    "apps.inquiries",
    "apps.cart",
    "apps.orders",
    "apps.constructor",
    "apps.payment",
]

DJANGO_APPS = [
    "jazzmin",
    "django_filters",
    'modeltranslation',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django.middleware.locale.LocaleMiddleware',
]

# settings.py

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'https://localhost:8080',
    'https://cardinar.uz',
    'http://cardinar.uz',
    'http://192.168.2.167:8080/'
]

CSRF_TRUSTED_ORIGINS = [
    "https://cardinar.uz",
    # Add other trusted origins as needed
]
CSRF_USE_SESSIONS = True
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'django.template.context_processors.i18n',
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'core/locale'),
]

LOCALE_DIRS = [
    os.path.join(BASE_DIR, 'core/locale')
]

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True
USE_TZ = True

LANGUAGE_CODE = "ru"
LANGUAGES = [
    ('ru', _('Russian')),
    ('uz', _('Uzbek'))
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/cardina1/api.cardinar.uz/cardinar/static'
STATICFILES_DIRS = [str(BASE_DIR) + "/assets", ]
MEDIA_URL = "/media/"
MEDIA_ROOT = '/home/cardina1/api.cardinar.uz/cardinar/media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.getenv("SECRET_KEY"),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",

    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=10),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    # "DEFAULT_THROTTLE_RATES": {
    #     "anon": "1/second",
    #     "user": "2/second",
    # },
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.JSONParser",
    ),
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "apps.users.authentication_backends.PhoneNumberAuthBackend",

]

LOGIN_URL = "users:user_login"
LOGOUT_URL = "users:user_logout"

AUTH_USER_MODEL = "users.User"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('SMTP_USERNAME')
EMAIL_HOST_PASSWORD = os.getenv('SMTP_PASSWORD')

PROVIDERS = {
    "payme": {
        "merchant_id": os.getenv('PAYME_MERCHANT_ID', None),
        "secret_key": os.getenv("PAYME_SECRET_KEY", None),
        "test_secret_key": os.getenv("PAYME_TEST_SECRET_KEY", None),
        "callback_url": "https://checkout.paycom.uz"
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',  # Set the desired log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),  # Set the path to the log file
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',  # Set the minimum log level to capture
    },
}

CSRF_COOKIE_AGE = 604800

STAGE = "develop"
