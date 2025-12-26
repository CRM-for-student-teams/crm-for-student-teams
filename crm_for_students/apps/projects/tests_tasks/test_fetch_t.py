from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.projects.models import Task


def test_task_fetch(auth_client_student_member, task: Task) -> None:
    """Good: Authenticated user fetches task"""
    response: Response = auth_client_student_member.get(f"/api/tasks/{task.id}/")
    assert response.status_code == HTTP_200_OK
    assert response.data["task"]["id"] == task.id
    assert response.data["task"]["title"] == task.title


def test_task_fetch_unauthenticated(api_client, task: Task) -> None:
    """Bad: Unauthenticated fetch"""
    response: Response = api_client.get(f"/api/tasks/{task.id}/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_task_fetch_not_found(auth_client_student_member) -> None:
    """Bad: Fetch non-existent task"""
    response: Response = auth_client_student_member.get("/api/tasks/999999/")
    assert response.status_code in (404, HTTP_400_BAD_REQUEST)


def test_task_fetch_forbidden(auth_client_student_captain, task: Task) -> None:
    """Bad: Forbidden fetch (simulate with wrong role)"""
    response: Response = auth_client_student_captain.get(f"/api/tasks/{task.id}/")
    assert response.status_code in (HTTP_401_UNAUTHORIZED, 403)
