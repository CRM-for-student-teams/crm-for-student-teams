from typing import Any

from django.db.models.query import QuerySet

from rest_framework.viewsets import ViewSet
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

from apps.projects.models import Project, Task
from apps.projects.serializers import ProjectSerializer, TaskSerializer
from apps.projects.permissions import IsProjectTeamMember


class ProjectsViewSet(ViewSet):
    """
    A viewser for managing projects.
    """

    # --------------------------------------------------------------
    # for permission handling
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsProjectTeamMember()]
        return [IsAuthenticated()]

    # --------------------------------------------------------------
    # for the proper swagger ui and doc
    def get_serializer_class(self):
        return ProjectSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if serializer_class:
            kwargs.setdefault("context", {"request": self.request, "view": self})
            return serializer_class(*args, **kwargs)
        return None

    def list(self, request: Request) -> Response:
        """
        List all projects.
        """
        projects = Project.objects.all()
        serializer: ProjectSerializer = ProjectSerializer(projects, many=True)
        return Response(
            data={
                "projects": serializer.data,
                "count": projects.count(),
                "details": "Projects fetched successfully!",
            },
            status=HTTP_200_OK,
        )

    def retrieve(self, requst: Request, pk: int) -> Response:
        """
        Retrieve a project by its ID.
        """
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response(
                data={"details": "Project not found."}, status=HTTP_404_NOT_FOUND
            )
        serializer: ProjectSerializer = ProjectSerializer(project)
        return Response(
            data={
                "project": serializer.data,
                "details": "Project fetched successfully!",
            },
            status=HTTP_200_OK,
        )

    def create(self, request: Request) -> Response:
        """
        Create a new project.
        """
        serializer: ProjectSerializer = ProjectSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "project": serializer.data,
                    "details": "Project created successfully!",
                },
                status=HTTP_201_CREATED,
            )
        return Response(
            data={
                "errors": serializer.errors,
                "details": "Project creation failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    def update(self, request: Request, pk: int) -> Response:
        """
        Update an existing project.
        """
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(
                data={"details": "Project not found."},
                status=HTTP_404_NOT_FOUND,
            )
        serializer: ProjectSerializer = ProjectSerializer(
            project, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "project": serializer.data,
                    "details": "Project updated successfully!",
                },
                status=HTTP_200_OK,
            )
        return Response(
            data={
                "errors": serializer.errors,
                "details": "Project update failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    def partial_update(self, request: Request, pk: int) -> Response:
        """
        Partially update an existing project.
        """
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(
                data={"details": "Project not found."},
                status=HTTP_404_NOT_FOUND,
            )
        serializer: ProjectSerializer = ProjectSerializer(
            project,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "project": serializer.data,
                    "details": "Project partially updated successfully!",
                },
                status=HTTP_200_OK,
            )
        return Response(
            data={
                "errors": serializer.errors,
                "details": "Project partial update failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        Delete a project.
        """
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(
                data={"details": "Project not found."},
                status=HTTP_404_NOT_FOUND,
            )
        project.delete()
        return Response(
            data={"details": "Project deleted successfully!"},
            status=HTTP_204_NO_CONTENT,
        )


class TasksViewSet(ViewSet):
    """
    A viewser for managing tasks.
    """

    pass
