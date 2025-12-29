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
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.projects.models import Project, Task
from apps.projects.serializers import (
    ProjectSerializer,
    TaskSerializer,
    ErrorResponseSerializer,
    ValidationErrorResponseSerializer,
)

from apps.projects.permissions import (
    IsStudentCaptain,
    IsStudentMember,
)


class ProjectsViewSet(ViewSet):
    """
    A viewser for managing projects.
    """

    # --------------------------------------------------------------
    # for permission handling
    def get_permissions(self):
        return [IsAuthenticated(), IsStudentCaptain()]

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
        operation_id="projects_list",
        summary="List all projects",
        description="Retrieve a paginated list of all projects. Returns project details including team information and member count.",
        tags=["Projects"],
        responses={HTTP_200_OK: ProjectSerializer(many=True)},
        examples=[
            OpenApiExample(
                "Success Response",
                value={
                    "projects": [
                        {
                            "id": 1,
                            "name": "Mobile App Development",
                            "description": "Building a cross-platform mobile application",
                            "deadline": "2025-12-31T23:59:59Z",
                            "team": 1,
                            "team_detail": {
                                "id": 1,
                                "name": "Tech Innovators",
                                "member_count": 5,
                            },
                            "created_at": "2025-01-01T10:00:00Z",
                            "updated_at": "2025-01-15T14:30:00Z",
                        }
                    ],
                    "count": 1,
                    "details": "Projects fetched successfully!",
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
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
        operation_id="projects_retrieve",
        summary="Retrieve a project by ID",
        description="Get detailed information about a specific project including team members and tasks.",
        tags=["Projects"],
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the project",
                required=True,
            ),
        ],
        responses={
            HTTP_200_OK: ProjectSerializer,
            HTTP_404_NOT_FOUND: ErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Success Response",
                value={
                    "project": {
                        "id": 1,
                        "name": "Mobile App Development",
                        "description": "Building a cross-platform mobile application",
                        "deadline": "2025-12-31T23:59:59Z",
                        "team": 1,
                        "team_detail": {
                            "id": 1,
                            "name": "Tech Innovators",
                            "member_count": 5,
                        },
                        "created_at": "2025-01-01T10:00:00Z",
                        "updated_at": "2025-01-15T14:30:00Z",
                    },
                    "details": "Project fetched successfully!",
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Not Found Error",
                value={"detail": "Project not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def retrieve(self, request: Request, pk: int) -> Response:
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
                data={"detail": "Project not found."}, status=HTTP_404_NOT_FOUND
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
        operation_id="projects_create",
        summary="Create a new project",
        description="Create a new project for a team. Only team captains can create projects.",
        tags=["Projects"],
        request=ProjectSerializer,
        responses={
            HTTP_201_CREATED: ProjectSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Create Project Request",
                value={
                    "name": "Mobile App Development",
                    "description": "Building a cross-platform mobile application",
                    "deadline": "2025-12-31T23:59:59Z",
                    "team": 1,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Success Response",
                value={
                    "project": {
                        "id": 1,
                        "name": "Mobile App Development",
                        "description": "Building a cross-platform mobile application",
                        "deadline": "2025-12-31T23:59:59Z",
                        "team": 1,
                        "created_at": "2025-01-01T10:00:00Z",
                        "updated_at": "2025-01-01T10:00:00Z",
                    },
                    "details": "Project created successfully!",
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Validation Error",
                value={
                    "errors": {
                        "name": ["This field is required."],
                        "team": ["This field is required."],
                    },
                    "detail": "Project creation failed!",
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
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
                "detail": "Project creation failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        operation_id="projects_update",
        summary="Update an existing project",
        description="Update all fields of an existing project. Only team captains can update projects.",
        tags=["Projects"],
        request=ProjectSerializer,
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the project to update",
                required=True,
            ),
        ],
        responses={
            HTTP_200_OK: ProjectSerializer,
            HTTP_404_NOT_FOUND: ErrorResponseSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def update(self, request: Request, pk: int) -> Response:
        """
        Update an existing project.
        """
        try:
            project = (
                Project.objects.select_related("team")
                .prefetch_related("team__members", "team__teammembership_set__user")
                .get(pk=pk)
            )
        except Project.DoesNotExist:
            return Response(
                data={"detail": "Project not found."},
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
                "detail": "Project update failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        operation_id="projects_partial_update",
        summary="Partially update an existing project",
        description="Update specific fields of an existing project. Only team captains can update projects.",
        tags=["Projects"],
        request=ProjectSerializer,
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the project to update",
                required=True,
            ),
        ],
        responses={
            HTTP_200_OK: ProjectSerializer,
            HTTP_404_NOT_FOUND: ErrorResponseSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Partial Update Request",
                value={"name": "Updated Project Name"},
                request_only=True,
            ),
        ],
    )
    def partial_update(self, request: Request, pk: int) -> Response:
        """
        Partially update an existing project.
        """
        try:
            project = (
                Project.objects.select_related("team")
                .prefetch_related("team__members", "team__teammembership_set__user")
                .get(pk=pk)
            )
        except Project.DoesNotExist:
            return Response(
                data={"detail": "Project not found."},
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
                "detail": "Project partial update failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        operation_id="projects_delete",
        summary="Delete a project",
        description="Permanently delete a project. Only team captains can delete projects. This action cannot be undone.",
        tags=["Projects"],
        parameters=[
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Unique identifier of the project to delete",
                required=True,
            ),
        ],
        responses={
            HTTP_204_NO_CONTENT: None,
            HTTP_404_NOT_FOUND: ErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Not Found Error",
                value={"detail": "Project not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def destroy(self, request: Request, pk: int) -> Response:
        """
        Delete a project.
        """
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(
                data={"detail": "Project not found."},
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
        # All task actions require student_member role
        return [IsAuthenticated(), IsStudentMember()]

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
        operation_id="tasks_list",
        summary="List all tasks",
        description="Retrieve a list of all tasks across all projects. Includes executor and project details.",
        tags=["Tasks"],
        responses={HTTP_200_OK: TaskSerializer(many=True)},
        examples=[
            OpenApiExample(
                "Success Response",
                value={
                    "tasks": [
                        {
                            "id": 1,
                            "title": "Design UI mockups",
                            "description": "Create initial UI designs",
                            "priority": 2,
                            "status": 1,
                            "executor": 5,
                            "project": 1,
                            "deadline": "2025-02-15T23:59:59Z",
                            "created_at": "2025-01-01T10:00:00Z",
                            "updated_at": "2025-01-10T15:30:00Z",
                        }
                    ],
                    "count": 1,
                    "details": "Tasks fetched successfully!",
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
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
            },
            status=HTTP_200_OK,
        )

    @extend_schema(
        summary="Retrieve a task by ID",
        responses={
            HTTP_200_OK: TaskSerializer,
            HTTP_404_NOT_FOUND: ErrorResponseSerializer,
        },
        description="Retrieve a task by its ID.",
        tags=["Tasks"],
    )
    def retrieve(self, request: Request, pk: int) -> Response:
        """
        Retrieve a task by its ID.
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
                data={"detail": "Task not found."}, status=HTTP_404_NOT_FOUND
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
        operation_id="tasks_create",
        summary="Create a new task",
        description="Create a new task within a project. Tasks can be assigned to team members.",
        tags=["Tasks"],
        request=TaskSerializer,
        responses={
            HTTP_201_CREATED: TaskSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Create Task Request",
                value={
                    "title": "Design UI mockups",
                    "description": "Create initial UI designs for the mobile app",
                    "priority": 2,
                    "project": 1,
                    "executor": 5,
                    "deadline": "2025-02-15T23:59:59Z",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Success Response",
                value={
                    "task": {
                        "id": 1,
                        "title": "Design UI mockups",
                        "description": "Create initial UI designs for the mobile app",
                        "priority": 2,
                        "status": 1,
                        "executor": 5,
                        "project": 1,
                        "deadline": "2025-02-15T23:59:59Z",
                        "created_at": "2025-01-01T10:00:00Z",
                        "updated_at": "2025-01-01T10:00:00Z",
                    },
                    "details": "Task created successfully!",
                },
                response_only=True,
                status_codes=["201"],
            ),
        ],
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
                "detail": "Task creation failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Update an existing task",
        request=TaskSerializer,
        responses={
            HTTP_200_OK: TaskSerializer,
            HTTP_404_NOT_FOUND: ErrorResponseSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
        description="Update an existing task.",
        tags=["Tasks"],
    )
    def update(self, request: Request, pk: int) -> Response:
        """
        Update an existing task.
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
                data={"detail": "Task not found."}, status=HTTP_404_NOT_FOUND
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
                "detail": "Task update failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Partially update an existing task",
        request=TaskSerializer,
        responses={
            HTTP_200_OK: TaskSerializer,
            HTTP_404_NOT_FOUND: ErrorResponseSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
        description="Partially update an existing task.",
        tags=["Tasks"],
    )
    def partial_update(self, request: Request, pk: int) -> Response:
        """
        Partially update an existing task.
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
                data={"detail": "Task not found."}, status=HTTP_404_NOT_FOUND
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
                "detail": "Task partial update failed!",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Delete a task",
        responses={
            HTTP_204_NO_CONTENT: None,
            HTTP_404_NOT_FOUND: ErrorResponseSerializer,
        },
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
                data={"detail": "Task not found."}, status=HTTP_404_NOT_FOUND
            )

        task.delete()
        return Response(
            data={"details": "Task deleted successfully!"},
            status=HTTP_204_NO_CONTENT,
        )
