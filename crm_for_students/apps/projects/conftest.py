from pytest import fixture

from apps.projects.models import Project, Task
from apps.teams.models import Team, TeamMembership


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
