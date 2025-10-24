from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from decouple import config

from settings.config import * # noqa F403

ROOT_URLCONF = "settings.urls"
WSGI_APPLICATION = "settings.wsgi.application"
ASGI_APPLICATION = "settings.asgi.application"

# --------------------------------
# Apps
# -----
DJANGO_AND_THIRD_PARTY_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
]
PROJECT_APPS = [
    "apps.clients",
    "apps.projects",
    "apps.teams",
]
INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS + PROJECT_APPS


# ----------------------------------------------------------------
# Middleware | Templates | Validators
# -----
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
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


# ----------------------------------------------------------------
# Internationalization
# -----
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = "/app/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# -------------------------------
# CORS Settings
# -------------------------------
CORS_ALLOWED_ORIGINS = (
    config("CORS_ALLOWED_ORIGINS", cast=str).split(",")
    if config("CORS_ALLOWED_ORIGINS", cast=str)
    else []
)

# Allow credentials (cookies, authorization headers)
CORS_ALLOW_CREDENTIALS = True

# Additional CORS settings
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


# ----------------------------------------------------------------
# Unfold Admin Panel Configuration
# -----

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
                        "link": reverse_lazy(
                            "admin:clients_client_changelist"
                        ),  # Заголовок кликабельный
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
