from typing import Any

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.teams.models import CustomUser


def test_project_create(
    user_student_captain: CustomUser, auth_client_student_captain, team
) -> None:
    """Good: Authenticated user creates project"""
    data: dict[str, Any] = {
        "name": "New Project",
        "description": "Description of the new project",
        "team": team.id,
    }
    response: Response = auth_client_student_captain.post("/api/projects/", data=data)
    assert response.status_code == HTTP_201_CREATED
    assert response.data["project"]["name"] == data["name"]
    assert response.data["project"]["description"] == data["description"]
    assert response.data["project"]["team_detail"]["id"] == data["team"]


def test_project_create_unauthenticated(api_client, team) -> None:
    """Bad: Unauthenticated create"""
    data = {"name": "Test", "description": "desc", "team": team.id}
    response: Response = api_client.post("/api/projects/", data=data)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_project_create_invalid_data(
    user_student_captain: CustomUser, auth_client_student_captain
) -> None:
    """Bad: Invalid data"""
    data: dict[str, Any] = {
        "name": "",
        "description": "Description of the new project",
        "team": 9999,
    }
    response: Response = auth_client_student_captain.post("/api/projects/", data=data)
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_project_create_forbidden(auth_client_student_member, team) -> None:
    """Bad: Forbidden create (simulate with wrong role)"""
    data = {"name": "Test", "description": "desc", "team": team.id}
    response: Response = auth_client_student_member.post("/api/projects/", data=data)
    assert response.status_code in (HTTP_401_UNAUTHORIZED, 403)
