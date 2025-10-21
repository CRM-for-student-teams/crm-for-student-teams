# Django modules

from pathlib import Path
import os
from distutils.util import strtobool


try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except Exception:
    pass


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-_q@qf2m8%l%#awm#i)(t+nbrkrw@_qs!%ysx@)$0^hya6$h9q=')

DEBUG = bool(strtobool(os.getenv('DJANGO_DEBUG', 'True')))

allowed = os.getenv('DJANGO_ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in allowed.split(',') if h.strip()] if allowed else []


ROOT_URLCONF = 'crm_for_students.urls'
WSGI_APPLICATION = 'crm_for_students.wsgi.application'
ASGI_APPLICATION = 'settings.asgi.application'


# ----------------------------------------------------------------
# Apps
# -----
DJANGO_AND_THIRD_PARTY_APPS = [
    "unfold",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]
PROJECT_APPS = [
    'clients',
    'projects',
    "teams",
]
INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS + PROJECT_APPS


# ----------------------------------------------------------------
# Middleware | Templates | Validators
# -----
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'student_crm'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}



# ----------------------------------------------------------------
# Internationalization
# -----
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# -------------------------------
# CORS Settings
# -------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://20.215.200.10",
    "https://20.215.200.10",
    "http://20.215.200.10:3000",
    "http://localhost:3000", 
    "http://localhost:8000",
]

# Allow credentials (cookies, authorization headers)
CORS_ALLOW_CREDENTIALS = True

# Additional CORS settings
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


#Unfold
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_HEADER": "Student Teams CRM",
    "SITE_TITLE": "Student Teams CRM",

    "SIDEBAR": {
        "show_search": True,
        "command_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Clients"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:clients_client_changelist"),  # Заголовок кликабельный
                    },

                    {
                        "title": _("Projects"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:projects_project_changelist"),
                    },

                    {
                        "title": _("Teams"),
                        "icon": "people",
                        "link": reverse_lazy("admin:teams_team_changelist"),
                    },
                ],
            },
        ],
    },

    "TABS": [
        {
            "models": [
                "clients.client",
                "clients.clientstage",
                "clients.activitylog",
            ],
            "items": [
                {
                    "title": _("All Clients"),
                    "link": reverse_lazy("admin:clients_client_changelist"),
                },
                {
                    "title": _("Client Stages"),
                    "link": reverse_lazy("admin:clients_clientstage_changelist"),
                },
                {
                    "title": _("Activity Logs"),
                    "link": reverse_lazy("admin:clients_activitylog_changelist"),
                },
            ],
        },
        {
            "models": [
                "projects.project",
                "projects.task",
            ],
            "items": [
                {
                    "title": _("Projects"),
                    "link": reverse_lazy("admin:projects_project_changelist"),
                },
                {
                    "title": _("Tasks"),
                    "link": reverse_lazy("admin:projects_task_changelist"),
                },
            ],
        },
        {
            "models": [
                "teams.team",
                "teams.teammembership",
                "teams.user",
            ],
            "items": [
                {
                    "title": _("Teams"),
                    "link": reverse_lazy("admin:teams_team_changelist"),
                },
                {
                    "title": _("Memberships"),
                    "link": reverse_lazy("admin:teams_teammembership_changelist"),
                },
                {
                    "title": _("Users"),
                    "link": reverse_lazy("admin:teams_user_changelist"),
                },
            ],
        },
    ],
}

