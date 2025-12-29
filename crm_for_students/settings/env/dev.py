# Python modules
from decouple import config

# Project modules
from settings.base import *  # noqa

DEBUG = True

# Add django-debug-toolbar only in dev
INSTALLED_APPS += ["debug_toolbar"]  # noqa
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa
ALLOWED_HOSTS = (
    config("DJANGO_ALLOWED_HOSTS", cast=str).split(",")
    if config("DJANGO_ALLOWED_HOSTS", cast=str)
    else []
)

# Django Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# Show Django Debug Toolbar for all requests (including API)
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    "RENDER_PANELS": True,
}

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
