from decouple import config

from settings.base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = (
    config("DJANGO_ALLOWED_HOSTS", cast=str).split(",")
    if config("DJANGO_ALLOWED_HOSTS", cast=str)
    else []
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", cast=str),
        "USER": config("DB_USER", cast=str),
        "PASSWORD": config("DB_PASSWORD", cast=str),
        "HOST": config("DB_HOST", cast=str),
        "PORT": config("DB_PORT", cast=str),
    }
}
