from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    DateTimeField,
)

from crm_for_students.apps.teams.models import CustomUser, Team


class TeamSerializer(ModelSerializer):
    """
    Serializer for the Team model.
    """

    id = CharField(read_only=True)
    name = CharField(max_length=200)
    description = CharField()
    created_at = DateTimeField(read_only=True)
    updated_at = DateTimeField(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]


class CustomUserSerializer(ModelSerializer):
    """
    Serializer for the CustomUser model.
    """

    id = CharField(read_only=True)
    email = CharField(max_length=150)
    full_name = CharField(max_length=240)
    created_at = DateTimeField(read_only=True)
    updated_at = DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "full_name",
            "created_at",
            "updated_at",
        ]