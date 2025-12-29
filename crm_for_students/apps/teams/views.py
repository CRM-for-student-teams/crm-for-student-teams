# Django modules
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet

# DRF modules
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework.request import Request

# Project modules
from apps.teams.models import Team, TeamMembership
from apps.teams.permissions import IsTeamCaptain, IsTeamMember
from apps.teams.serializers import (
    TeamListSerializer,
    TeamMembershipSerialier,
    TeamSerializer,
    ValidationErrorResponseSerializer,
)


class TeamViewSet(ViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get_queryset(self) -> QuerySet[Team]:
        return Team.objects.all()

    def get_object(self, pk: int) -> Team:
        return get_object_or_404(Team, pk=pk)

    def get_serializer_class(self) -> type:
        if self.action == "list":
            return TeamListSerializer
        return TeamSerializer

    def get_permissions(self) -> list:
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsTeamCaptain()]
        elif self.action == "retrieve":
            return [IsAuthenticated(), IsTeamMember()]
        return [IsAuthenticated()]

    @extend_schema(
        operation_id="teams_list",
        summary="List all teams",
        description="Retrieve a complete list of all teams in the system. Returns basic team information including member count.",
        tags=["Teams"],
        responses={HTTP_200_OK: TeamListSerializer(many=True)},
        examples=[
            OpenApiExample(
                "Success Response",
                value=[
                    {
                        "id": 1,
                        "name": "Tech Innovators",
                        "description": "Building the future",
                        "member_count": 5,
                        "inserted_at": "2025-01-01T10:00:00Z",
                    },
                    {
                        "id": 2,
                        "name": "Code Warriors",
                        "description": "Excellence in coding",
                        "member_count": 3,
                        "inserted_at": "2025-01-05T14:30:00Z",
                    },
                ],
                response_only=True,
                status_codes=["200"],
            ),
        ],
    )
    def list(self, request: Request) -> Response:
        teams = self.get_queryset().prefetch_related(
            "members", "teammembership_set__user"
        )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(teams, many=True)
        return Response(serializer.data)

    @extend_schema(
        operation_id="teams_retrieve",
        summary="Retrieve team details",
        description="Get detailed information about a specific team including all members and their roles. Only team members can access this endpoint.",
        tags=["Teams"],
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the team",
                required=True,
            ),
        ],
        responses={HTTP_200_OK: TeamSerializer},
        examples=[
            OpenApiExample(
                "Team Details",
                value={
                    "id": 1,
                    "name": "Tech Innovators",
                    "description": "A team focused on innovation",
                    "inserted_at": "2025-01-01T10:00:00Z",
                    "updated_at": "2025-01-15T12:00:00Z",
                    "members": [
                        {
                            "id": 1,
                            "email": "captain@example.com",
                            "full_name": "John Doe",
                            "role": "student",
                        },
                        {
                            "id": 2,
                            "email": "member@example.com",
                            "full_name": "Jane Smith",
                            "role": "student",
                        },
                    ],
                    "memberships": [
                        {
                            "id": 1,
                            "role": "student_captain",
                            "user": {
                                "id": 1,
                                "email": "captain@example.com",
                                "full_name": "John Doe",
                            },
                        }
                    ],
                    "member_count": 5,
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    )
    def retrieve(self, request: Request, pk: int = None) -> Response:
        team = get_object_or_404(
            Team.objects.prefetch_related("members", "teammembership_set__user"), pk=pk
        )
        self.check_object_permissions(request, team)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    @extend_schema(
        operation_id="teams_create",
        summary="Create a new team",
        description="Create a new team. The creator automatically becomes the team captain with full permissions.",
        tags=["Teams"],
        request=TeamSerializer,
        responses={
            HTTP_201_CREATED: TeamSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Create Team Request",
                value={
                    "name": "Tech Innovators",
                    "description": "A team focused on cutting-edge technology",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Success Response",
                value={
                    "id": 1,
                    "name": "Tech Innovators",
                    "description": "A team focused on cutting-edge technology",
                    "inserted_at": "2025-01-01T10:00:00Z",
                    "updated_at": "2025-01-01T10:00:00Z",
                    "members": [],
                    "memberships": [],
                    "member_count": 1,
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Validation Error",
                value={
                    "name": ["This field is required."],
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    )
    def create(self, request: Request) -> Response:
        serializer = TeamSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        team = serializer.save()

        TeamMembership.objects.create(
            team=team, user=request.user, role="student_captain"
        )

        return Response(serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        operation_id="teams_update",
        summary="Update team information",
        description="Update all fields of a team. Only team captains can update team information.",
        tags=["Teams"],
        request=TeamSerializer,
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the team to update",
                required=True,
            ),
        ],
        responses={
            HTTP_200_OK: TeamSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def update(self, request: Request, pk: int = None) -> Response:
        team = self.get_object(pk)
        self.check_object_permissions(request, team)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            team, data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        operation_id="teams_partial_update",
        summary="Partially update team",
        description="Update specific fields of a team. Only team captains can update team information.",
        tags=["Teams"],
        request=TeamSerializer,
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the team to update",
                required=True,
            ),
        ],
        responses={
            HTTP_200_OK: TeamSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Update Name Only",
                value={"name": "Updated Team Name"},
                request_only=True,
            ),
            OpenApiExample(
                "Update Description Only",
                value={"description": "Updated team description"},
                request_only=True,
            ),
        ],
    )
    def partial_update(self, request: Request, pk: int = None) -> Response:
        team = self.get_object(pk)
        self.check_object_permissions(request, team)
        serializer = TeamSerializer(team, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        operation_id="teams_delete",
        summary="Delete a team",
        description="Permanently delete a team and all associated data. Only team captains can delete teams. This action cannot be undone.",
        tags=["Teams"],
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the team to delete",
                required=True,
            ),
        ],
        responses={HTTP_204_NO_CONTENT: None},
    )
    def destroy(self, request: Request, pk: int = None) -> Response:
        team = self.get_object(pk)
        self.check_object_permissions(request, team)

        team.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        operation_id="teams_my_teams",
        summary="Get my teams",
        description="Retrieve a list of all teams where the authenticated user is a member. Returns teams with basic information and member count.",
        tags=["Teams"],
        responses={HTTP_200_OK: TeamListSerializer(many=True)},
        examples=[
            OpenApiExample(
                "User's Teams",
                value=[
                    {
                        "id": 1,
                        "name": "Tech Innovators",
                        "description": "My main team",
                        "member_count": 5,
                        "inserted_at": "2025-01-01T10:00:00Z",
                    },
                    {
                        "id": 3,
                        "name": "Side Project",
                        "description": "Weekend project team",
                        "member_count": 2,
                        "inserted_at": "2025-01-10T15:00:00Z",
                    },
                ],
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "No Teams",
                value=[],
                response_only=True,
                status_codes=["200"],
            ),
        ],
    )
    @action(detail=False, methods=["get"])
    def my_teams(self, request: Request) -> Response:
        teams = Team.objects.filter(members=request.user).prefetch_related(
            "members", "teammembership_set__user"
        )
        serializer = TeamListSerializer(teams, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        operation_id="teams_leave",
        summary="Leave a team",
        description="""Allow a user to leave a team.
        
        **Restrictions:**
        - Team captains cannot leave their team
        - Must be a member of the team to leave
        
        **Note:** To transfer captain role before leaving, update the membership roles first.
        """,
        request=None,
        tags=["Teams"],
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the team to leave",
                required=True,
            ),
        ],
        responses={
            HTTP_200_OK: OpenApiResponse(description="Successfully left the team"),
            HTTP_400_BAD_REQUEST: OpenApiResponse(description="Error occurred"),
        },
        examples=[
            OpenApiExample(
                "Success Response",
                value={"message": "You have successfully left the team."},
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Captain Cannot Leave",
                value={"detail": "The team captain cannot leave the team."},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Not a Member",
                value={"detail": "You are not a member of this team."},
                response_only=True,
                status_codes=["400"],
            ),
        ],
    )
    @action(detail=True, methods=["post"])
    def leave_team(self, request: Request, pk: int = None) -> Response:
        team = self.get_object(pk)

        is_captain = TeamMembership.objects.filter(
            team=team,
            user=request.user,
            role="student_captain",
        ).exists()

        if is_captain:
            return Response(
                {"detail": "The team captain cannot leave the team."},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            membership = TeamMembership.objects.get(team=team, user=request.user)
            membership.delete()

            return Response(
                {"message": "You have successfully left the team."}, status=HTTP_200_OK
            )
        except TeamMembership.DoesNotExist:
            return Response(
                {"detail": "You are not a member of this team."},
                status=HTTP_400_BAD_REQUEST,
            )


class TeamMembershipViewSet(ViewSet):
    serializer_class = TeamMembershipSerialier
    queryset = TeamMembership.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Retrieve permissions",
        responses={HTTP_200_OK: OpenApiResponse(description="Permissions retrieved")},
        description="Retrieve permissions depending on action",
        tags=["Permissions"],
    )
    def get_permissions(self) -> list:
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsTeamCaptain()]
        elif self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsTeamMember()]
        return [IsAuthenticated()]

    def get_queryset(self) -> QuerySet[TeamMembership]:
        return TeamMembership.objects.all()

    def get_object(self, pk: int) -> TeamMembership:
        return get_object_or_404(TeamMembership, pk=pk)

    @extend_schema(
        operation_id="team_memberships_list",
        summary="List all team memberships",
        description="Retrieve a complete list of all team memberships across all teams. Shows user details and their role in each team.",
        tags=["TeamMembership"],
        responses={HTTP_200_OK: TeamMembershipSerialier(many=True)},
        examples=[
            OpenApiExample(
                "Memberships List",
                value=[
                    {
                        "id": 1,
                        "team": 1,
                        "team_name": "Tech Innovators",
                        "role": "student_captain",
                        "user": {
                            "id": 1,
                            "email": "captain@example.com",
                            "full_name": "John Doe",
                            "role": "student",
                        },
                        "inserted_at": "2025-01-01T10:00:00Z",
                        "updated_at": "2025-01-01T10:00:00Z",
                    },
                    {
                        "id": 2,
                        "team": 1,
                        "team_name": "Tech Innovators",
                        "role": "student_member",
                        "user": {
                            "id": 2,
                            "email": "member@example.com",
                            "full_name": "Jane Smith",
                            "role": "student",
                        },
                        "inserted_at": "2025-01-02T14:00:00Z",
                        "updated_at": "2025-01-02T14:00:00Z",
                    },
                ],
                response_only=True,
                status_codes=["200"],
            ),
        ],
    )
    def list(self, request: Request) -> Response:
        queryset = self.get_queryset().select_related("user", "team")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        operation_id="team_memberships_retrieve",
        summary="Retrieve team membership details",
        description="Get detailed information about a specific team membership including user and team details.",
        tags=["TeamMembership"],
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the team membership",
                required=True,
            ),
        ],
        responses={HTTP_200_OK: TeamMembershipSerialier},
    )
    def retrieve(self, request: Request, pk: int = None) -> Response:
        membership = get_object_or_404(
            TeamMembership.objects.select_related("user", "team"), pk=pk
        )
        self.check_object_permissions(request, membership)

        serializer = self.serializer_class(membership)
        return Response(serializer.data)

    @extend_schema(
        operation_id="team_memberships_create",
        summary="Add a member to team",
        description="""Add a new member to a team with a specific role.
        
        **Permissions:**
        - Only team captains can add members
        - Cannot add a user who is already a member
        
        **Available Roles:**
        - `student_captain`: Full permissions
        - `student_member`: Regular member
        """,
        request=TeamMembershipSerialier,
        tags=["TeamMembership"],
        responses={
            HTTP_201_CREATED: TeamMembershipSerialier,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Add Member Request",
                value={"team": 1, "user_id": 5, "role": "student_member"},
                request_only=True,
            ),
            OpenApiExample(
                "Success Response",
                value={
                    "id": 3,
                    "team": 1,
                    "team_name": "Tech Innovators",
                    "role": "student_member",
                    "user": {
                        "id": 5,
                        "email": "newmember@example.com",
                        "full_name": "Alice Johnson",
                        "role": "student",
                    },
                    "inserted_at": "2025-01-15T10:00:00Z",
                    "updated_at": "2025-01-15T10:00:00Z",
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Already a Member Error",
                value={"error": "This user is already a member of the team"},
                response_only=True,
                status_codes=["400"],
            ),
        ],
    )
    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.validated_data["team"]

        is_captain = TeamMembership.objects.filter(
            team=team,
            user=request.user,
            role="student_captain",
        ).exists()

        if not is_captain:
            raise PermissionDenied("Only team captain can add members")

        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        operation_id="team_memberships_update",
        summary="Update team membership",
        description="Update team membership details including role changes. Only team captains can update memberships.",
        request=TeamMembershipSerialier,
        tags=["TeamMembership"],
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the team membership to update",
                required=True,
            ),
        ],
        responses={
            HTTP_200_OK: TeamMembershipSerialier,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def update(self, request: Request, pk: int = None) -> Response:
        membership = self.get_object(pk)
        self.check_object_permissions(request, membership)

        serializer = self.serializer_class(membership, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        operation_id="team_memberships_partial_update",
        summary="Partially update team membership",
        description="Update specific fields of a team membership, such as changing a member's role. Only team captains can update memberships.",
        request=TeamMembershipSerialier,
        tags=["TeamMembership"],
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the team membership to update",
                required=True,
            ),
        ],
        responses={
            HTTP_200_OK: TeamMembershipSerialier,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Change Role to Captain",
                value={"role": "student_captain"},
                request_only=True,
            ),
            OpenApiExample(
                "Change Role to Member",
                value={"role": "student_member"},
                request_only=True,
            ),
        ],
    )
    def partial_update(self, request: Request, pk: int = None) -> Response:
        membership = self.get_object(pk)
        self.check_object_permissions(request, membership)

        serializer = self.serializer_class(membership, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        operation_id="team_memberships_delete",
        summary="Remove team member",
        description="Remove a member from a team. Only team captains can remove members. This action cannot be undone.",
        tags=["TeamMembership"],
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the team membership to delete",
                required=True,
            ),
        ],
        responses={HTTP_204_NO_CONTENT: None},
    )
    def destroy(self, request: Request, pk: int = None) -> Response:
        membership = self.get_object(pk)
        self.check_object_permissions(request, membership)

        membership.delete()
        return Response(status=HTTP_204_NO_CONTENT)
