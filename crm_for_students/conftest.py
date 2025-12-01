from pytest import fixture

from rest_framework.test import APIClient

from apps.project.models import Project, Task
from apps.teams.models import CustomUser, Team


# ---------------------------------------------------------------------------
# Users

@fixture
def user_client(db) -> CustomUser:
    return CustomUser.objects.create_user(
        email="client@test.com",
        password="12345",
        full_name="Client Clientovich",
        role="client",
    )

@fixture
def user_student_member(db) ->  CustomUser:
    return CustomUser.objects.create_user(
        email="student_member@test.com",
        password="12345",
        full_name="Student Member",
        role="student_member",
    )

@fixture
def user_student_captain(db) ->  CustomUser:
    return CustomUser.objects.create_user(
        email="student_captain@test.com",
        password="123455",
        full_name="Student Captain",
        role="student_captain",
    )


# ---------------------------------------------------------------------------
# API Client
@fixture 
def api_client() -> APIClient:
    return APIClient()


# ---------------------------------------------------------------------------
# Authenticated API Clients

@fixture
def auth_client_client(
    api_client: APIClient,
    user_client: CustomUser,
) -> APIClient:
    api_client.force_authenticate(user=user_client)
    return api_client

@fixture 
def auth_client_student_member(
    api_client: APIClient,
    user_student_member: CustomUser,
) -> APIClient:
    api_client.force_authenticate(user=user_student_member)
    return api_client

@fixture 
def auth_client_student_captain(
    api_client: APIClient,
    user_student_captain: CustomUser,
) -> APIClient:
    api_client.force_authenticate(user=user_student_captain)
    return api_client


