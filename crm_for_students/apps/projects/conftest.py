from pytest import fixture

from apps.projects.models import Project, Task
from conftest import (
    api_client,
    auth_client_client,
    auth_client_student_captain,
    auth_client_student_member,
    user_client,
    user_student_captain,
    user_student_member,
)

@fixture
def project(db, user_student_captain) -> Project:
    return Project.objects.create(
        name="Test Project",
        description="A project for testing purposes",
        captain=user_student_captain,
    )

@fixture
def task(db, user_student_member, project) -> Task:
    return Task.objects.create(
        title="Test Task",
        description="A task for testing purposes",
        assigned_to=user_student_member,
        project=project,
    )












