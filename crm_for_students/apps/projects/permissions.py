# DRF modules
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

# Project modules
from apps.projects.models import Project


class IsProjectTeamMember(BasePermission):
    """
    Custom permission to only allow members of the project's team to access it.
    """

    def has_object_permission(self, request: Request, view: View, obj: Project) -> bool:
        """
        Docstring for has_object_permission

        :param self: Description
        :param request: Description
        :type request: Request
        :param view: Description
        :type view: View
        :param obj: Object that we are checking has permission to or not
        :type obj: Project
        :return:  it has the permission
        :rtype: bool
        """
        return request.user in obj.team.members.all()


class IsStudentCaptain(BasePermission):
    """
    Permission to only allow student captains to access projects.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.user.role == "student_captain"


class IsStudentMember(BasePermission):
    """
    Permission to only allow student members to access tasks.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.user.role == "student_member"
