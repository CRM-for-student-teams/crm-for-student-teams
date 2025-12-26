from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.projects.models import Project
from apps.teams.models import CustomUser


def test_project_fetch(
    auth_client_student_captain, user_student_captain: CustomUser, project: Project
) -> None:
    """Good: Authenticated user fetches project"""
    response: Response = auth_client_student_captain.get(f"/api/projects/{project.id}/")
    assert response.status_code == HTTP_200_OK
    assert response.data["project"]["id"] == project.id
    assert response.data["project"]["name"] == project.name


def test_project_fetch_unauthenticated(api_client, project: Project) -> None:
    """Bad: Unauthenticated fetch"""
    response: Response = api_client.get(f"/api/projects/{project.id}/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_project_fetch_not_found(auth_client_student_captain) -> None:
    """Bad: Fetch non-existent project"""
    response: Response = auth_client_student_captain.get("/api/projects/999999/")
    assert response.status_code in (404, HTTP_400_BAD_REQUEST)


def test_project_fetch_forbidden(auth_client_student_member, project: Project) -> None:
    """Bad: Forbidden fetch (simulate with wrong role)"""
    response: Response = auth_client_student_member.get(f"/api/projects/{project.id}/")
    assert response.status_code in (HTTP_401_UNAUTHORIZED, 403)