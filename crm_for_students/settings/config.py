import os
from distutils.util import strtobool

DEBUG = bool(strtobool(os.getenv("DJANGO_DEBUG", "True")))
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
