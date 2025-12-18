# Django modules
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

# Project modules
from apps.teams.models import Team


NAME_MAX_LENGTH = 100
TITLE_MAX_LENGTH = 100


class Project(Model):
    """
    Model representing a project within the CRM system.
    """

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
        """
        Docstring for Meta
        """

        db_table = "projects"
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        """
        Docstring for __str__

        :param self: Description
        :return: Description
        :rtype: str
        """
        return self.name


class Task(Model):
    """
    Model representing a task within a project.
    """

    LOW_I = 1
    MEDIUM_I = 2
    HIGH_I = 3
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

    PRIORITY_CHOICES = (
        (LOW_I, LOW),
        (MEDIUM_I, MEDIUM),
        (HIGH_I, HIGH),
    )

    TODO_I = 1
    IN_PROGRESS_I = 2
    DONE_I = 3
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

    STATUS_CHOICES = (
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
        to=settings.AUTH_USER_MODEL,
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
        """
        Docstring for Meta
        """
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self) -> str:
        """
        Docstring for __str__

        :param self: Description
        :return: Description
        :rtype: str
        """
        return f"{self.title} ({self.get_status_display()})"

    def get_status_display(self) -> str:
        """
        Docstring for get_status_display

        :param self: Description
        :return: Description
        :rtype: str
        """
        return dict(self.STATUS_CHOICES).get(self.status, "Unknown")
