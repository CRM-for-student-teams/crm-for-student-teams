from rest_framework.response import Response

from conftest import (
    api_client,
    auth_client_client,
    auth_client_student_captain,
    auth_client_student_member,
    user_client,
    user_student_captain,
    user_student_member,
)


from apps.projects.models import Project, Task
from apps.teams.models import CustomUser
from apps.projects.conftest import project, task


def test_project_list(auth_client_student_captain):
    response: Response = auth_client_student_captain.get("/api/projects/")
    assert response.status_code == 200


def test_project_list_unauthenticated(api_client):
    response: Response = api_client.get("/api/projects/")
    assert response.status_code == 401


def test_project_fetch(auth_client_student_captain, user_student_captain, project):
    response: Response = auth_client_student_captain.get(f"/api/projects/{project.id}/")
    assert response.status_code == 200
    assert response.data["project"]["id"] == project.id
    assert response.data["project"]["name"] == project.name


def test_project_fetch_unauthenticated(api_client, user_student_captain):
    response: Response = api_client.get(f"/api/projects/{user_student_captain.id}/")
    assert response.status_code == 401


def test_project_create(user_student_captain, auth_client_student_captain):
    pass


def test_project_create_invalid_data(user_student_captain, auth_client_student_captain):
    pass


def test_project_update(user_student_captain, auth_client_student_captain, project):
    pass


def test_project_update_invalid_data(
    user_student_captain, auth_client_student_captain, project
):
    pass


def test_project_delete(user_student_captain, auth_client_student_captain, project):
    pass


def test_project_delete_unauthenticated(api_client, project):
    pass


def test_task_list():
    pass


def test_task_list_unauthenticated(api_client, user_student_member):
    pass


def test_task_fetch():
    pass


def test_task_create(user_student_member, auth_client_student_member):
    pass


def test_task_update(user_student_member, auth_client_student_member, task):
    pass


def test_task_delete(user_student_member, auth_client_student_member, task):
    pass
