from typing import Any

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.projects.models import Project, Task
from apps.teams.models import CustomUser


def test_project_list(auth_client_student_captain) -> None:
    response: Response = auth_client_student_captain.get("/api/projects/")
    assert response.status_code == HTTP_200_OK


def test_project_list_unauthenticated(api_client) -> None:
    response: Response = api_client.get("/api/projects/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_project_fetch(
    auth_client_student_captain, user_student_captain: CustomUser, project: Project
) -> None:
    response: Response = auth_client_student_captain.get(f"/api/projects/{project.id}/")
    assert response.status_code == HTTP_200_OK
    assert response.data["project"]["id"] == project.id
    assert response.data["project"]["name"] == project.name


def test_project_fetch_unauthenticated(
    api_client, user_student_captain: CustomUser
) -> None:
    response: Response = api_client.get(f"/api/projects/{user_student_captain.id}/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_project_create(
    user_student_captain: CustomUser, auth_client_student_captain, team
) -> None:
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


def test_project_create_invalid_data(
    user_student_captain: CustomUser, auth_client_student_captain
) -> None:

    data: dict[str, Any] = {
        "name": "",
        "description": "Description of the new project",
        "team": 9999,
    }
    response: Response = auth_client_student_captain.post("/api/projects/", data=data)
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_project_update(
    user_student_captain: CustomUser, auth_client_student_captain, project: Project
) -> None:
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


def test_project_update_invalid_data(
    user_student_captain: CustomUser, auth_client_student_captain, project: Project
) -> None:
    data: dict[str, Any] = {
        "name": "",
        "description": "Updated description",
        "team": 9999,
    }
    response: Response = auth_client_student_captain.put(
        f"/api/projects/{project.id}/", data=data
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_project_delete(
    user_student_captain: CustomUser, auth_client_student_captain, project: Project
) -> None:
    response: Response = auth_client_student_captain.delete(
        f"/api/projects/{project.id}/"
    )
    assert response.status_code == HTTP_204_NO_CONTENT
    assert not Project.objects.filter(id=project.id).exists()


def test_project_delete_unauthenticated(api_client, project: Project) -> None:
    response: Response = api_client.delete(f"/api/projects/{project.id}/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_task_list(auth_client_student_member) -> None:
    response: Response = auth_client_student_member.get("/api/tasks/")
    assert response.status_code == HTTP_200_OK


def test_task_list_unauthenticated(api_client, user_student_member: CustomUser) -> None:
    response: Response = api_client.get("/api/tasks/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_task_fetch(auth_client_student_member, task: Task) -> None:
    response: Response = auth_client_student_member.get(f"/api/tasks/{task.id}/")
    assert response.status_code == HTTP_200_OK
    assert response.data["task"]["id"] == task.id
    assert response.data["task"]["title"] == task.title


def test_task_fetch_unauthenticated(api_client, task: Task) -> None:
    response: Response = api_client.get(f"/api/tasks/{task.id}/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_task_create(
    user_student_member: CustomUser, auth_client_student_member, project: Project
) -> None:
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


def test_task_create_invalid_data(
    user_student_member: CustomUser, auth_client_student_member
) -> None:
    data: dict[str, Any] = {
        "title": "",
        "description": "Description of the new task",
        "executor": 9999,
        "project": 9999,
    }
    response: Response = auth_client_student_member.post("/api/tasks/", data=data)
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_task_update(auth_client_student_member, task: Task) -> None:
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


def test_task_update_invalid_data(auth_client_student_member, task: Task) -> None:
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


def test_task_delete(
    user_student_member: CustomUser, auth_client_student_member, task: Task
) -> None:
    response: Response = auth_client_student_member.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == HTTP_204_NO_CONTENT
    assert not Task.objects.filter(id=task.id).exists()
