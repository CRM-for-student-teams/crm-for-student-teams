# Django modules
from django.contrib import admin
from django.urls import path, include

# DRF modules
from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    path("admin/", admin.site.urls),
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
    path("api/", include("apps.teams.urls"))
]
