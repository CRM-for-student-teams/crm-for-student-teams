from typing import Any

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.projects.models import Project
from apps.teams.models import CustomUser


def test_task_create(
    user_student_member: CustomUser, auth_client_student_member, project: Project
) -> None:
    """Good: Authenticated user creates task"""
    data: dict[str, Any] = {
        "title": "New Task",
        "description": "Description of the new task",
        "executor": user_student_member.id,
        "project": project.id,
    }
    response: Response = auth_client_student_member.post("/api/tasks/", data=data)
    assert response.status_code == HTTP_201_CREATED
    assert response.data["task"]["title"] == "New Task"
    assert response.data["task"]["description"] == "Description of the new task"
    assert response.data["task"]["executor_detail"]["id"] == user_student_member.id
    assert response.data["task"]["project_detail"]["id"] == project.id


def test_task_create_unauthenticated(
    api_client, user_student_member: CustomUser, project: Project
) -> None:
    """Bad: Unauthenticated create"""
    data = {
        "title": "Test",
        "description": "desc",
        "executor": user_student_member.id,
        "project": project.id,
    }
    response: Response = api_client.post("/api/tasks/", data=data)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_task_create_invalid_data(
    user_student_member: CustomUser, auth_client_student_member
) -> None:
    """Bad: Invalid data"""
    data: dict[str, Any] = {
        "title": "",
        "description": "Description of the new task",
        "executor": 9999,
        "project": 9999,
    }
    response: Response = auth_client_student_member.post("/api/tasks/", data=data)
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_task_create_forbidden(
    auth_client_student_captain, user_student_member: CustomUser, project: Project
) -> None:
    """Bad: Forbidden create (simulate with wrong role)"""
    data = {
        "title": "Test",
        "description": "desc",
        "executor": user_student_member.id,
        "project": project.id,
    }
    response: Response = auth_client_student_captain.post("/api/tasks/", data=data)
    assert response.status_code in (HTTP_401_UNAUTHORIZED, 403)
