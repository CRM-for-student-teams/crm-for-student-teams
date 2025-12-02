# apps/teams/permissions.py
from rest_framework.permissions import BasePermission
from apps.teams.models import TeamMembership


class IsTeamCaptain(BasePermission):
    """
    Permission to check if user is a team captain
    """

    def has_permission(self, request, view):
        """
        Global permission check - user must be authenticated
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check
        """
        if hasattr(obj, 'team'):
            team = obj.team
        else:
            team = obj

        return TeamMembership.objects.filter(
            team=team,
            user=request.user,
            role='student_captain'
        ).exists()


class IsTeamMember(BasePermission):
    """
    Permission to check if user is a member of the team
    """

    def has_permission(self, request, view):
        """
        Global permission check - user must be authenticated
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check
        """
        if hasattr(obj, 'team'):
            team = obj.team
        else:
            team = obj

        return TeamMembership.objects.filter(
            team=team,
            user=request.user
        ).exists()
