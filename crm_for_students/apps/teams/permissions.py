# DRF modules
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View
# Project modules
from apps.teams.models import TeamMembership

class IsTeamCaptain(BasePermission):
    """
    Permission to check if user is the team captain or not
    """

    def has_object_permission(self, request: Request, view: View, obj):
        if hasattr(obj, "id"):
            team_id = obj.id
        elif hasattr(obj, "team"):
            team_id = obj.team.id
        else:
            return False
        return TeamMembership.objects.filter(
            user = request.user,
            team_id = team_id,
            role = "student_captain"
        ).exists()
    
class IsTeamMember(BasePermission):
    """
    Permission to check if user is the team member
    """

    def has_object_permission(self, request: Request, view: View, obj):
        if hasattr(obj, "members"):
            return obj.members.filter(id=request.user.id).exists()
        if hasattr(obj,"team"):
            return obj.team.members.filter(id=request.user.id).exists()
        return False