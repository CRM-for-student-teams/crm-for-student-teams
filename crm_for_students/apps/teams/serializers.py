# DRF modules
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    PrimaryKeyRelatedField,
    ValidationError,
    SerializerMethodField,
    Serializer,
)

# Project modules
from apps.teams.models import CustomUser, Team, TeamMembership


class CustomUserSerializer(ModelSerializer):
    """
    Serializer for the CustomUser model.
    """

    class Meta:
        """
        Docstring for Meta
        """
        model = CustomUser
        fields = [
            "id",
            "email",
            "full_name",
            "inserted_at",
            "updated_at",
            "role",
        ]


class TeamMembershipSerialier(ModelSerializer):
    """
    Serializer for team membership
    """

    user = CustomUserSerializer(read_only=True)

    user_id = PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source="user",
        write_only=True,
    )

    team_name = CharField(source="team.name", read_only=True)

    class Meta:
        """
        Docstring for Meta
        """
        model = TeamMembership
        fields = [
            "id",
            "team",
            "role",
            "inserted_at",
            "updated_at",
            "user",
            "user_id",
            "team_name",
        ]
        read_only_fields = ["id", "inserted_at", "updated_at"]

    def validate(self, data):
        """
        Docstring for validate

        :param self: Description
        :param data: Description
        """
        team = data.get("team")
        user = data.get("user")

        if team and user:
            if TeamMembership.objects.filter(team=team, user=user).exists():
                raise ValidationError("This user is already a member of the team")
        return data


class TeamSerializer(ModelSerializer):
    """
    Serializer for the Team model.
    """

    members = CustomUserSerializer(many=True, read_only=True)
    memberships = TeamMembershipSerialier(
        source="teammembership_set",
        many=True,
        read_only=True,
    )
    member_count = SerializerMethodField()

    class Meta:
        """
        Docstring for Meta
        """
        model = Team
        fields = [
            "id",
            "name",
            "description",
            "inserted_at",
            "updated_at",
            "members",
            "memberships",
            "member_count",
        ]
        read_only_field = ["id", "inserted_at", "updated_at"]

    def get_member_count(self, obj):
        """
        Gets the number of the team members

        :param self: Description
        :param obj: Description
        """
        return obj.members.count()

    def create(self, validated_data):
        """
        Creates a teammembership object

        :param self: Description
        :param validated_data: Description
        """

        request = self.context.get("request")
        team = Team.objects.create(**validated_data)

        TeamMembership.objects.create(
            team=team,
            user=request.user,
            role="studen_captain",
        )
        return team


class TeamListSerializer(ModelSerializer):
    """
    Serializer for team list
    """

    member_count = SerializerMethodField()

    class Meta:
        """
        Docstring for Meta
        """
        model = Team
        fields = [
            "id",
            "name",
            "description",
            "member_count",
            "inserted_at",
        ]
        read_only_fields = fields

    def get_member_count(self, obj):
        """
        Retuns count of the members

        :param self: Description
        :param obj: Description
        """
        return obj.members.count()


class ErrorResponseSerializer(Serializer):
    """Serializer for error responses"""

    detail = CharField(help_text="Error message describing what went wrong")

    class Meta:
        ref_name = "TeamErrorResponse"


class ValidationErrorResponseSerializer(Serializer):
    """Serializer for validation error responses"""

    error = CharField(help_text="Validation error message")

    class Meta:
        ref_name = "TeamValidationErrorResponse"