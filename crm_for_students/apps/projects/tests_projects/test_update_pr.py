from typing import Any

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.projects.models import Project
from apps.teams.models import CustomUser


def test_project_update(
    user_student_captain: CustomUser, auth_client_student_captain, project: Project
) -> None:
    """Good: Authenticated user updates project"""
    data: dict[str, Any] = {
        "name": "Updated Project Name",
        "description": "Updated description",
        "team": project.team.id,
    }
    response: Response = auth_client_student_captain.put(
        f"/api/projects/{project.id}/", data=data
    )
    assert response.status_code == HTTP_200_OK
    assert response.data["project"]["name"] == data["name"]
    assert response.data["project"]["description"] == data["description"]


def test_project_update_unauthenticated(api_client, project: Project) -> None:
    """Bad: Unauthenticated update"""
    data = {"name": "Test", "description": "desc", "team": 1}
    response: Response = api_client.put(f"/api/projects/{project.id}/", data=data)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_project_update_invalid_data(
    user_student_captain: CustomUser, auth_client_student_captain, project: Project
) -> None:
    """Bad: Invalid data"""
    data: dict[str, Any] = {
        "name": "",
        "description": "Updated description",
        "team": 9999,
    }
    response: Response = auth_client_student_captain.put(
        f"/api/projects/{project.id}/", data=data
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_project_update_forbidden(auth_client_student_member, project: Project) -> None:
    """Bad: Forbidden update (simulate with wrong role)"""
    data = {"name": "Test", "description": "desc", "team": project.team.id}
    response: Response = auth_client_student_member.put(
        f"/api/projects/{project.id}/", data=data
    )
    assert response.status_code in (HTTP_401_UNAUTHORIZED, 403)