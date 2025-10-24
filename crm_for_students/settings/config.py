from decouple import config


ENV_POSSIBLE_OPTIONS = ("dev", "prod")
ENV_ID = config("DJANGO_ENV_ID", cast=str)
SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str)
