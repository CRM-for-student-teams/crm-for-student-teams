from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.projects.models import Task
from apps.teams.models import CustomUser


def test_task_delete(
    user_student_member: CustomUser, auth_client_student_member, task: Task
) -> None:
    """Good: Authenticated user deletes task"""
    response: Response = auth_client_student_member.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == HTTP_204_NO_CONTENT
    assert not Task.objects.filter(id=task.id).exists()


def test_task_delete_unauthenticated(api_client, task: Task) -> None:
    """Bad: Unauthenticated delete"""
    response: Response = api_client.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_task_delete_not_found(auth_client_student_member) -> None:
    """Bad: Delete non-existent task"""
    response: Response = auth_client_student_member.delete("/api/tasks/999999/")
    assert response.status_code in (404, HTTP_400_BAD_REQUEST)


def test_task_delete_forbidden(auth_client_student_captain, task: Task) -> None:
    """Bad: Forbidden delete (simulate with wrong role)"""
    response: Response = auth_client_student_captain.delete(f"/api/tasks/{task.id}/")
    assert response.status_code in (HTTP_401_UNAUTHORIZED, 403)
