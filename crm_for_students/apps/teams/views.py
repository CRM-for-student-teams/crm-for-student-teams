from typing import Any

from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from apps.teams.models import Team, TeamMembership, CustomUser
from apps.projects.serializers import ProjectSerializer, TaskSerializer
from apps.projects.permissions import IsProjectTeamMember
from apps.teams.permissions import IsTeamCaptain, IsTeamMember
from apps.teams.serializers import TeamListSerializer, TeamMembershipSerialier, TeamSerializer


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = []

    filterset_fields = ["members"]
    serach_fields = ["name", "description"]
    ordering_fields = ["inserted_at", "name"]
    ordering = ["-inserted_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return TeamListSerializer
        return TeamSerializer
    
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsTeamCaptain()]
        elif self.action in ["retrieve"]:
            return [IsAuthenticated(), IsTeamMember()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=["get"])
    def my_teams(self, request):
        teams = Team.objects.filter(members=request.user)
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def leave_team(self, request, pk=None):
        team = self.get_objects()

        is_captain = TeamMembership.objects.filter(
            team=team,
            user=request.user,
            role="student_captain"
        ).exists()
        if is_captain:
            return Response(
                {"error": "Team leader can't leave the team"},
                status=HTTP_400_BAD_REQUEST
            )
        
        try:
            membership = TeamMembership.objects.get(team=team, user=request.user)
            membership.delete()
            return Response(
                {"message": "You successfully left the team"},
                status=HTTP_200_OK
            )
        except TeamMembership.DoesNotExist:
            return Response(
                {"error": "You are not member of the team"},
                status=HTTP_400_BAD_REQUEST
            )
        

class TeamMembershipViewSet(ModelViewSet):
    queryset = TeamMembership.objects.all()
    serializer_class = TeamMembershipSerialier
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_field = ["team", "user", "role"]
    ordering_fields = ["inserted_at"]
    ordering = ["-inserted_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsTeamCaptain()]
        elif self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsTeamMember()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        team = serializer.validated_data["team"]

        is_captain = TeamMembership.objects.filter(
            team=team,
            user=self.request.user,
            role="student_captain",
        )

        if not is_captain:
            raise PermissionDenied("Only team captain can add members")
        serializer.save()