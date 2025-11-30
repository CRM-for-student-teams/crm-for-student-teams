from typing import Any

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.projects.models import Project, Task
from apps.projects.serializers import ProjectSerializer, TeaskSerializer


