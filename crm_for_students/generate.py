# Python modules
import random
# Django modules
from django.utils import timezone
# Project modules
from apps.teams.models import CustomUser, Team, TeamMembership
from apps.projects.models import Project, Task

roles = ["student_captain", "student_member", "client"]

users = []
for i in range(10):
    user = CustomUser.objects.create_user(
        email=f"user{i}@example.com",
        full_name=f"User {i}",
        password="Password123",
        role=random.choice(roles),   # type: ignore
    )
    users.append(user)

teams = []
for i in range(5):
    team = Team.objects.create(
        name=f"Team {i}",
        description=f"Description for Team {i}",
    )
    teams.append(team)

for team in teams:
    captain = random.choice(users)
    TeamMembership.objects.create(
        team=team,
        user=captain,
        role="student_captain"
    )
    for member in random.sample(users, 2):
        if member != captain:
            TeamMembership.objects.create(
                team=team,
                user=member,
                role="student_member"
            )

projects = []
for team in teams:
    for i in range(5):
        project = Project.objects.create(
            name=f"Project {i} of {team.name}",
            description=f"Project {i} description",
            team=team,
            deadline=timezone.now() + timezone.timedelta(days=30)
        )
        projects.append(project)

status_choices = [1, 2, 3]
priority_choices = [1, 2, 3]

for project in projects:
    for i in range(4):
        Task.objects.create(
            title=f"Task {i} for {project.name}",
            description=f"Description for Task {i}",
            project=project,
            executor=random.choice(users),
            priority=random.choice(priority_choices),
            status=random.choice(status_choices),
            deadline=timezone.now() + timezone.timedelta(days=random.randint(1, 30))
        )

print("Test data generation complete!")
