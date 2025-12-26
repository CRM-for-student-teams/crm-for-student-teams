from typing import Any

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.projects.models import Task


def test_task_update(auth_client_student_member, task: Task) -> None:
    """Good: Authenticated user updates task"""
    data: dict[str, Any] = {
        "title": "Updated Task Title",
        "description": "Updated description",
        "executor": task.executor.id,
        "project": task.project.id,
    }
    response: Response = auth_client_student_member.put(
        f"/api/tasks/{task.id}/", data=data
    )
    assert response.status_code == HTTP_200_OK
    assert response.data["task"]["title"] == data["title"]
    assert response.data["task"]["description"] == data["description"]


def test_task_update_unauthenticated(api_client, task: Task) -> None:
    """Bad: Unauthenticated update"""
    data = {"title": "Test", "description": "desc", "executor": 1, "project": 1}
    response: Response = api_client.put(f"/api/tasks/{task.id}/", data=data)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_task_update_invalid_data(auth_client_student_member, task: Task) -> None:
    """Bad: Invalid data"""
    data: dict[str, Any] = {
        "title": "",
        "description": "Updated description",
        "executor": 9999,
        "project": 9999,
    }
    response: Response = auth_client_student_member.put(
        f"/api/tasks/{task.id}/", data=data
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_task_update_forbidden(auth_client_student_captain, task: Task) -> None:
    """Bad: Forbidden update (simulate with wrong role)"""
    data = {
        "title": "Test",
        "description": "desc",
        "executor": task.executor.id,
        "project": task.project.id,
    }
    response: Response = auth_client_student_captain.put(
        f"/api/tasks/{task.id}/", data=data
    )
    assert response.status_code in (HTTP_401_UNAUTHORIZED, 403)
