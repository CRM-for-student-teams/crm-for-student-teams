from pytest import fixture

from apps.projects.models import Project, Task
from apps.teams.models import Team, TeamMembership
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
def team(db, user_student_captain) -> Team:
    team: Team = Team.objects.create(
        name="Test Team",
        description="A team for testing purposes",
    )
    TeamMembership.objects.create(
        user=user_student_captain,
        team=team,
        role="student_captain",
    )
    return team


@fixture
def project(db, team) -> Project:
    return Project.objects.create(
        name="Test Project",
        description="A project for testing purposes",
        team=team,
    )


@fixture
def task(db, user_student_member, project) -> Task:
    return Task.objects.create(
        title="Test Task",
        description="A task for testing purposes",
        executor=user_student_member,
        project=project,
    )
