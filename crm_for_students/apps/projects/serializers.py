# DRF modules
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
    CharField,
)

# Project modules
from apps.projects.models import Project, Task
from apps.teams.models import Team, CustomUser
from apps.teams.serializers import TeamSerializer, CustomUserSerializer


class ProjectSerializer(ModelSerializer):
    """Serializer for the Project model."""

    team_detail = TeamSerializer(source="team", read_only=True)
    team = PrimaryKeyRelatedField(queryset=Team.objects.all(), write_only=True)

    class Meta:
        """
        Docstring for Meta
        """
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "team",
            "team_detail",
            "deadline",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TaskSerializer(ModelSerializer):
    """Serializer for the Task model."""

    executor_detail = CustomUserSerializer(source="executor", read_only=True)
    executor = PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )
    project_detail = ProjectSerializer(source="project", read_only=True)
    project = PrimaryKeyRelatedField(queryset=Project.objects.all(), write_only=True)

    class Meta:
        """
        Docstring for Meta
        """
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "executor",
            "executor_detail",
            "priority",
            "project",
            "project_detail",
            "deadline",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ErrorResponseSerializer(Serializer):
    """Serializer for error responses"""

    detail = CharField(help_text="Error message describing what went wrong")

    class Meta:
        ref_name = "ProjectErrorResponse"


class ValidationErrorResponseSerializer(Serializer):
    """Serializer for validation error responses"""

    errors = CharField(help_text="Validation errors")
    detail = CharField(help_text="Error message")

    class Meta:
        ref_name = "ProjectValidationErrorResponse"
