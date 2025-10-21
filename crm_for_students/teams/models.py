# Django modules
from django.db import models
from django.utils import timezone
from django.conf import settings


class User(models.Model):
    """
    Represents a user in the system.
    """
    ROLE_CHOICES = [
        ("captain", "Captain"),
        ("member", "Member"),
    ]

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    inserted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return f"{self.name}"


class Team(models.Model):
    """
    Represents a team within the system.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    inserted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(
        User,
        through="TeamMembership",
        related_name="teams",
        verbose_name="members"
    )

    class Meta:
        db_table = "team"
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self) -> str:
        return f"{self.name}"


class TeamMembership(models.Model):
    """
    Intermediate model for linking users to teams with a specific role.
    """
    ROLE_CHOICES = [
        ("captain", "Captain"),
        ("member", "Member"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    inserted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "team_membership"
        verbose_name = "Team membership"
        verbose_name_plural = "Teams membership"

    def __str__(self) -> str:
        return f"{self.user.name} -> {self.team.name} (role: {self.role})"
