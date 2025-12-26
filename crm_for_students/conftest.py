from pytest import fixture
from django.conf import settings

from rest_framework.test import APIClient

from apps.teams.models import CustomUser


@fixture(scope="session", autouse=True)
def disable_debug_toolbar():
    """Disable debug_toolbar during tests to avoid static files issues."""
    settings.DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: False}
    # Remove debug toolbar middleware if present
    if "debug_toolbar.middleware.DebugToolbarMiddleware" in settings.MIDDLEWARE:
        settings.MIDDLEWARE = [
            mw for mw in settings.MIDDLEWARE 
            if mw != "debug_toolbar.middleware.DebugToolbarMiddleware"
        ]

# ---------------------------------------------------------------------------
# Users


@fixture
def user_client(db):
    return CustomUser.objects.create_user(
        email="client@test.com",
        password="12345",
        full_name="Client Clientovich",
        role="client",
    )


@fixture
def user_student_member(db):
    return CustomUser.objects.create_user(
        email="student_member@test.com",
        password="12345",
        full_name="Student Member",
        role="student_member",
    )


@fixture
def user_student_captain(db):
    return CustomUser.objects.create_user(
        email="student_captain@test.com",
        password="123455",
        full_name="Student Captain",
        role="student_captain",
    )


# ---------------------------------------------------------------------------
# API Client
@fixture
def api_client():
    return APIClient()


# ---------------------------------------------------------------------------
# Authenticated API Clients


@fixture
def auth_client_client(
    api_client,
    user_client,
):
    api_client.force_authenticate(user=user_client)
    return api_client


@fixture
def auth_client_student_member(
    api_client,
    user_student_member,
):
    api_client.force_authenticate(user=user_student_member)
    return api_client


@fixture
def auth_client_student_captain(
    api_client,
    user_student_captain,
):
    api_client.force_authenticate(user=user_student_captain)
    return api_client
