from django.contrib import admin

from common.admin import BaseModelAdmin
from .models import Client, ClientStage, ActivityLog


class ActivityLogInline(admin.TabularInline):
    """
    Inline admin interface for displaying and managing activity logs
    directly from the Client admin page.
    """
    model = ActivityLog
    extra = 1  # Number of empty activity log rows shown by default
    readonly_fields = ('inserted_at',)  # Prevent editing the timestamp


@admin.register(Client)
class ClientAdmin(BaseModelAdmin):
    """
    Admin interface for managing Client records.

    Allows filtering by stage and team, searching by name or email,
    and viewing related activity logs inline.
    """
    list_display = ('fullname', 'email', 'phone_number', 'stage', 'team')
    list_filter = ('stage', 'team')
    search_fields = ('fullname', 'email')
    inlines = [ActivityLogInline]


@admin.register(ClientStage)
class ClientStageAdmin(BaseModelAdmin):
    """
    Admin interface for managing ClientStage records.

    Displays the numeric status field representing the client stage.
    """
    list_display = ('status',)


@admin.register(ActivityLog)
class ActivityLogAdmin(BaseModelAdmin):
    """
    Admin interface for viewing and filtering activity logs.

    Supports filtering by date, client, and user,
    and searching by client name, user name, or action content.
    """
    list_display = ('user', 'client', 'action', 'inserted_at')
    list_filter = ('inserted_at', 'client', 'user')
    search_fields = ('client__fullname', 'action', 'user__username')
