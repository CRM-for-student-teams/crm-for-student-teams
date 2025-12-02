# Third Party
from typing import Any

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    DateTimeField,
)

# Local Modules
from apps.teams.models import CustomUser, Team


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


class UserCRUDSerializer(ModelSerializer):
    """
    Serializer for creating and updating CustomUser instances.
    Handles password hashing and optional updates.
    """

    password = CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "password",
                  "role", "id", "inserted_at", "updated_at"]
        read_only_fields = ["id", "inserted_at", "updated_at"]

    def create(self, validated_data: dict[str, Any]) -> CustomUser:
        """
        Create a new user with hashed password.
        """
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance: CustomUser, validated_data: dict[str, Any]) -> CustomUser:
        """
        Update user fields. Hash password if provided.
        """
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
