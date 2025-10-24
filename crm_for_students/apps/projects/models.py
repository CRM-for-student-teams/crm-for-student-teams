from django.db.models import (
    Model,
    IntegerField,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    CASCADE,
    SET_NULL,
)
from django.conf import settings
from django.utils import timezone

from apps.teams.models import Team, User


class Project(Model):
    """
    Model representing a project within the CRM system.
    """

    NAME_MAX_LENGTH: int = 100

    name = CharField(max_length=NAME_MAX_LENGTH)
    description = TextField(null=True, blank=True)
    deadline = DateTimeField(null=True, blank=True)
    team = ForeignKey(
        to=Team,
        on_delete=CASCADE,
        related_name="projects",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        return self.name


class Task(Model):
    """
    Model representing a task within a project.
    """

    TITLE_MAX_LENGTH: int = 100

    LOW_I: int = 1
    MEDIUM_I: int = 2
    HIGH_I: int = 3
    LOW: str = "Low"
    MEDIUM: str = "Medium"
    HIGH: str = "High"

    PRIORITY_CHOICES: tuple[tuple[int, str]] = (
        (LOW_I, LOW),
        (MEDIUM_I, MEDIUM),
        (HIGH_I, HIGH),
    )

    TODO_I: int = 1
    IN_PROGRESS_I: int = 2
    DONE_I: int = 3
    TODO: str = "To Do"
    IN_PROGRESS: str = "In Progress"
    DONE: str = "Done"

    STATUS_CHOICES: tuple[tuple[int, str]] = (
        (TODO_I, TODO),
        (IN_PROGRESS_I, IN_PROGRESS),
        (DONE_I, DONE),
    )

    title = CharField(max_length=TITLE_MAX_LENGTH)
    description = TextField(blank=True)
    project = ForeignKey(
        to=Project,
        on_delete=CASCADE,
        related_name="tasks",
    )
    executor = ForeignKey(
        to=User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    priority = IntegerField(
        choices=PRIORITY_CHOICES,
        default=MEDIUM_I,
    )
    status = IntegerField(
        choices=STATUS_CHOICES,
        default=TODO_I,
    )
    deadline = DateTimeField(null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self) -> str:
        return f"{self.title} ({self.get_status_display()})"

    def get_status_display(self) -> str:
        return dict(self.STATUS_CHOICES).get(self.status, "Unknown")
