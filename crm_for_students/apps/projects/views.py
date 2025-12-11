# DRF modules
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

# Project modules
from drf_spectacular.utils import extend_schema

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

    @extend_schema(
        responses={200: ProjectSerializer(many=True)},
        description="Retrieve a list of all projects.",
        tags=["Projects"],
    )
    def list(self, request: Request) -> Response:
        """
        List all projects.
        """
        projects = (
            Project.objects.select_related("team")
            .prefetch_related("team__members", "team__teammembership_set__user")
            .all()
        )
        serializer: ProjectSerializer = ProjectSerializer(projects, many=True)
        return Response(
            data={
                "projects": serializer.data,
                "count": projects.count(),
                "details": "Projects fetched successfully!",
            },
            status=HTTP_200_OK,
        )

    @extend_schema(
        responses={200: ProjectSerializer, 404: None},
        description="Retrieve a project by its ID.",
        tags=["Projects"],
    )
    def retrieve(self, requst: Request, pk: int) -> Response:
        """
        Retrieve a project by its ID.
        """
        try:
            project = (
                Project.objects.select_related("team")
                .prefetch_related("team__members", "team__teammembership_set__user")
                .get(id=pk)
            )
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

    @extend_schema(
        request=ProjectSerializer,
        responses={201: ProjectSerializer, 400: None},
        description="Create a new project.",
        tags=["Projects"],
    )
    def create(self, request: Request) -> Response:
        """
        Create a new project.
        """
        serializer: ProjectSerializer = ProjectSerializer(data=request.data)
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

    @extend_schema(
        request=ProjectSerializer,
        responses={200: ProjectSerializer, 404: None, 400: None},
        description="Update an existing project.",
        tags=["Projects"],
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

    @extend_schema(
        request=ProjectSerializer,
        responses={200: ProjectSerializer, 404: None, 400: None},
        description="Partially update an existing project.",
        tags=["Projects"],
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

    @extend_schema(
        responses={204: None, 404: None},
        description="Delete a project.",
        tags=["Projects"],
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

    # --------------------------------------------------------------
    # for permission handling
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsProjectTeamMember()]
        return [IsAuthenticated()]

    # --------------------------------------------------------------
    # for the proper swagger ui and doc
    def get_serializer_class(self):
        return TaskSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if serializer_class:
            kwargs.setdefault("context", {"request": self.request, "view": self})
            return serializer_class(*args, **kwargs)
        return None

    @extend_schema(
        responses={200: TaskSerializer(many=True)},
        description="List all tasks.",
        tags=["Tasks"],
    )
    def list(self, request: Request) -> Response:
        """
        List all tasks.
        """

        tasks = (
            Task.objects.select_related("executor", "project__team")
            .prefetch_related(
                "project__team__members", "project__team__teammembership_set__user"
            )
            .all()
        )
        serializer: TaskSerializer = TaskSerializer(tasks, many=True)

        return Response(
            data={
                "tasks": serializer.data,
                "count": tasks.count(),
                "details": "Tasks fetched successfully!",
                "status": HTTP_200_OK,
            }
        )

    @extend_schema(
        responses={200: TaskSerializer, 404: None},
        description="Retrieve a task by its ID.",
        tags=["Tasks"],
    )
    def retrieve(self, request: Request, pk: int) -> Response:
        """
        Reetrieve a task by its ID.
        """

        try:
            task = (
                Task.objects.select_related("executor", "project__team")
                .prefetch_related(
                    "project__team__members", "project__team__teammembership_set__user"
                )
                .get(id=pk)
            )
        except Task.DoesNotExist:
            return Response(
                data={"details": "Task not found."}, status=HTTP_404_NOT_FOUND
            )

        serializer: TaskSerializer = TaskSerializer(task)
        return Response(
            data={
                "task": serializer.data,
                "details": "Task fetched successfully!",
            },
            status=HTTP_200_OK,
        )

    @extend_schema(
        request=TaskSerializer,
        responses={201: TaskSerializer, 400: None},
        description="Create a new task.",
        tags=["Tasks"],
    )
    def create(self, request: Request) -> Response:
        """
        Create a new task.
        """

        serializer: TaskSerializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "task": serializer.data,
                    "details": "Task created successfully!",
                },
                status=HTTP_201_CREATED,
            )
        return Response(
            data={
                "errors": serializer.errors,
                "details": "Task creation failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        request=TaskSerializer,
        responses={200: TaskSerializer, 404: None, 400: None},
        description="Update an existing task.",
        tags=["Tasks"],
    )
    def update(self, request: Request, pk: int) -> Response:
        """
        Update an existing task.
        """

        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response(
                data={"details": "Task not found."}, status=HTTP_404_NOT_FOUND
            )

        serializer: TaskSerializer = TaskSerializer(
            task, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "task": serializer.data,
                    "details": "Task updated successfully!",
                },
                status=HTTP_200_OK,
            )
        return Response(
            data={
                "errors": serializer.errors,
                "details": "Task update failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        request=TaskSerializer,
        responses={200: TaskSerializer, 404: None, 400: None},
        description="Partially update an existing task.",
        tags=["Tasks"],
    )
    def partial_update(self, request: Request, pk: int) -> Response:
        """
        Partially update an existing task.
        """

        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response(
                data={"details": "Task not found."}, status=HTTP_404_NOT_FOUND
            )

        serializer: TaskSerializer = TaskSerializer(
            task, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "task": serializer.data,
                    "details": "Task partially updated successfully!",
                },
                status=HTTP_200_OK,
            )
        return Response(
            data={
                "errors": serializer.errors,
                "details": "Task partial update failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        responses={204: None, 404: None},
        description="Delete a task by its ID.",
        tags=["Tasks"],
    )
    def destroy(self, request: Request, pk: int) -> Response:
        """
        Delete a task
        """

        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response(
                data={"details": "Task not found."}, status=HTTP_404_NOT_FOUND
            )

        task.delete()
        return Response(
            data={"details": "Task deleted successfully!"},
            status=HTTP_204_NO_CONTENT,
        )
