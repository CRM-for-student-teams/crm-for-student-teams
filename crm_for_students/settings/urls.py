# Django modules
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import JsonResponse

# DRF modules
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


def home_view(request):
    """Main hello"""
    return JsonResponse(
        {
            "message": "Welcome to the student teams freelance system!",
            "version": "1.0.0",
            "endpoints": {
                "admin": "/admin/",
                "api_docs": {
                    "swagger": "/api/docs/swagger-ui/",
                    "redoc": "/api/docs/redoc/",
                    "schema": "/api/schema/",
                },
                "api": {
                    "teams": "/api/teams/",
                    "projects": "/api/projects/",
                    "auth": {
                        "register": "/api/auth/register/",
                        "login": "/api/auth/login/",
                        "refresh": "/api/auth/token/refresh/",
                    },
                },
            },
        }
    )


urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/",
        include(
            [
                path("", include("apps.teams.urls")),
                path("", include("apps.projects.urls")),
            ]
        ),
    ),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
