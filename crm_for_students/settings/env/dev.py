from decouple import config

from settings.base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = (
    config("DJANGO_ALLOWED_HOSTS", cast=str).split(",")
    if config("DJANGO_ALLOWED_HOSTS", cast=str)
    else []
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="postgres", cast=str),
        "USER": config("DB_USER", default="postgres", cast=str),
        "PASSWORD": config("DB_PASSWORD", default="postgres", cast=str),
        "HOST": config("DB_HOST", default="localhost", cast=str),
        "PORT": config("DB_PORT", default="5432", cast=str),
    }
}
