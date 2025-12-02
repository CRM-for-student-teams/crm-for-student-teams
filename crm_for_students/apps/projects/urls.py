from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.projects.views import ProjectsViewSet, TasksViewSet


router: DefaultRouter = DefaultRouter()

router.register(prefix="projects", viewset=ProjectsViewSet, basename="projects")
router.register(prefix="tasks", viewset=TasksViewSet, basename="tasks")

urlpatterns = [
    path("", include(router.urls)),
]
