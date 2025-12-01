from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

from apps.projects.models import Project


class IsProjectTeamMember(BasePermission):
    """
    Custom permission to only allow members of the project's team to access it.
    """

    def has_object_permission(self, request: Request, view: View, obj: Project) -> bool:
        return request.user in obj.team.members.all()
    
