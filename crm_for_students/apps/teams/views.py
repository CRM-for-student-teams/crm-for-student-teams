# Django modules
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

# DRF modules
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
from rest_framework.request import Request

# Project modules
from apps.teams.models import Team, TeamMembership
from apps.teams.permissions import IsTeamCaptain, IsTeamMember
from apps.teams.serializers import (
    TeamListSerializer,
    TeamMembershipSerialier,
    TeamSerializer,
)


class TeamViewSet(ViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get_queryset(self) -> "QuerySet[Team]":
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
        summary="List all teams",
        description="Returns a list of all teams",
        tags=["Teams"],
        responses={200: TeamListSerializer(many=True)},
    )
    def list(self, request: Request) -> Response:
        teams = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(teams, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Retrieve team",
        description="Returns detailed information about a specific team",
        tags=["Teams"],
        responses={200: TeamSerializer},
    )
    def retrieve(self, request: Request, pk: int = None) -> Response:
        team = self.get_object(pk)
        self.check_object_permissions(request, team)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a team",
        description="Creates a new team",
        tags=["Teams"],
        request=TeamSerializer,
        responses={201: TeamSerializer},
    )
    def create(self, request: Request) -> Response:
        serializer = TeamSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        team = serializer.save()

        TeamMembership.objects.create(
            team=team, user=request.user, role="student_captain"
        )

        return Response(serializer.data, status=201)

    @extend_schema(
        summary="Update team",
        tags=["Teams"],
        request=TeamSerializer,
        responses={200: TeamSerializer},
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
        summary="Partially update team",
        tags=["Teams"],
        request=TeamSerializer,
        responses={200: TeamSerializer},
    )
    def partial_update(self, request: Request, pk: int = None) -> Response:
        team = self.get_object(pk)
        self.check_object_permissions(request, team)
        serializer = TeamSerializer(team, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete a team",
        tags=["Teams"],
        responses={204: None},
    )
    def destroy(self, request: Request, pk: int = None) -> Response:
        team = self.get_object(pk)
        self.check_object_permissions(request, team)

        team.delete()
        return Response(status=204)

    @extend_schema(
        summary="Get my teams",
        description="Returns a list of teams the authenticated user is a member of",
        tags=["Teams"],
        responses={200: TeamListSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def my_teams(self, request: Request) -> Response:
        teams = Team.objects.filter(members=request.user)
        serializer = TeamListSerializer(teams, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        summary="Leave a team",
        description=(
            "Allows a user to leave a team. " "Captains cannot leave their team"
        ),
        request=None,
        tags=["Teams"],
        responses={
            200: OpenApiResponse(description="Successfully left the team"),
            400: OpenApiResponse(description="Error occurred"),
        },
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
                {"error": "The team captain cannot leave the team."}, status=400
            )

        try:
            membership = TeamMembership.objects.get(team=team, user=request.user)
            membership.delete()

            return Response(
                {"message": "You have successfully left the team."}, status=200
            )
        except TeamMembership.DoesNotExist:
            return Response({"error": "You are not a member of this team."}, status=400)


class TeamMembershipViewSet(ViewSet):
    serializer_class = TeamMembershipSerialier
    queryset = TeamMembership.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: OpenApiResponse(description="Permissions retrieved")},
        description="Retrieve permissions depending on action",
        tags=["Permissions"],
    )
    def get_permissions(self) -> list:
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsTeamCaptain()]
        elif self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsTeamMember()]
        return [IsAuthenticated()]

    def get_queryset(self) -> "QuerySet[TeamMembership]":
        return TeamMembership.objects.all()

    def get_object(self, pk: int) -> TeamMembership:
        return get_object_or_404(TeamMembership, pk=pk)

    @extend_schema(
        summary="List all team members",
        description="Returns a list of all team memberships",
        tags=["TeamMembership"],
        responses={200: TeamMembershipSerialier(many=True)},
    )
    def list(self, request: Request) -> Response:
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Retrieve a team member",
        description="Returns details of a specific team membership",
        tags=["TeamMembership"],
        responses={200: TeamMembershipSerialier},
    )
    def retrieve(self, request: Request, pk: int = None) -> Response:
        membership = self.get_object(pk)
        self.check_object_permissions(request, membership)

        serializer = self.serializer_class(membership)
        return Response(serializer.data)

    @extend_schema(
        summary="Add a team member",
        description="Only team captains can add members to the team",
        request=TeamMembershipSerialier,
        tags=["TeamMembership"],
        responses={201: TeamMembershipSerialier},
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
        return Response(serializer.data, status=201)

    @extend_schema(
        summary="Update a team member",
        description="Update a team membership",
        request=TeamMembershipSerialier,
        tags=["TeamMembership"],
        responses={200: TeamMembershipSerialier},
    )
    def update(self, request: Request, pk: int = None) -> Response:
        membership = self.get_object(pk)
        self.check_object_permissions(request, membership)

        serializer = self.serializer_class(membership, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Partially update a team member",
        description="Partially update a team membership",
        request=TeamMembershipSerialier,
        tags=["TeamMembership"],
        responses={200: TeamMembershipSerialier},
    )
    def partial_update(self, request: Request, pk: int = None) -> Response:
        membership = self.get_object(pk)
        self.check_object_permissions(request, membership)

        serializer = self.serializer_class(membership, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete a team member",
        description="Deletes a specific team membership",
        tags=["TeamMembership"],
        responses={204: None},
    )
    def destroy(self, request: Request, pk: int = None) -> Response:
        membership = self.get_object(pk)
        self.check_object_permissions(request, membership)

        membership.delete()
        return Response(status=HTTP_204_NO_CONTENT)
