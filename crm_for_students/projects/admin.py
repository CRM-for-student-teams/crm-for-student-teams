from django.contrib import admin

from common.admin import BaseModelAdmin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'team', 'deadline', 'created_at', 'updated_at')
    search_fields = ('name', 'team__name')
    list_filter = ('created_at', 'updated_at', 'deadline')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Task)
class TaskAdmin(BaseModelAdmin):
    list_display = ('id', 'title', 'project', 'priority', 'status', 'deadline', 'created_at', 'updated_at')
    search_fields = ('title', 'project__name', 'executor__username')
    list_filter = ('priority', 'status', 'created_at', 'updated_at', 'deadline')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
