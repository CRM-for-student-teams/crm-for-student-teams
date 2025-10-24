"""
WSGI config for crm_for_students project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from settings.config import ENV_ID, ENV_POSSIBLE_OPTIONS


assert (
    ENV_ID in ENV_POSSIBLE_OPTIONS
), f"Set correct DJANGORLAR_ENV_ID env var. Possible options: {ENV_POSSIBLE_OPTIONS}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"settings.env.{ENV_ID}")

application = get_wsgi_application()
