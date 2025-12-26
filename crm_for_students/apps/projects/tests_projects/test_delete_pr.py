from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.projects.models import Project
from apps.teams.models import CustomUser


def test_project_delete(
    user_student_captain: CustomUser, auth_client_student_captain, project: Project
) -> None:
    """Good: Authenticated user deletes project"""
    response: Response = auth_client_student_captain.delete(
        f"/api/projects/{project.id}/"
    )
    assert response.status_code == HTTP_204_NO_CONTENT
    assert not Project.objects.filter(id=project.id).exists()


def test_project_delete_unauthenticated(api_client, project: Project) -> None:
    """Bad: Unauthenticated delete"""
    response: Response = api_client.delete(f"/api/projects/{project.id}/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_project_delete_not_found(auth_client_student_captain) -> None:
    """Bad: Delete non-existent project"""
    response: Response = auth_client_student_captain.delete("/api/projects/999999/")
    assert response.status_code in (404, HTTP_400_BAD_REQUEST)


def test_project_delete_forbidden(auth_client_student_member, project: Project) -> None:
    """Bad: Forbidden delete (simulate with wrong role)"""
    response: Response = auth_client_student_member.delete(
        f"/api/projects/{project.id}/"
    )
    assert response.status_code in (HTTP_401_UNAUTHORIZED, 403)