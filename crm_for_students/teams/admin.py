# Django modules
from django.contrib import admin

from common.admin import BaseModelAdmin

# Project modules
from .models import User, Team, TeamMembership


class TeamMembershipInline(admin.TabularInline):
    """
    Inline admin interface for adding, viewing team members
    directly within the Team admin page.
    """

    model = TeamMembership
    extra = 1
    verbose_name = "Member"
    verbose_name_plural = "Members"


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    """
    Admin interface for managing User records.
    """

    list_display = ("name", "role", "email", "inserted_at", "updated_at")
    list_filter = ("role", "name")
    search_fields = ("name", "email")
    readonly_fields = ("inserted_at",)
    ordering = ("name",)
    list_per_page = 30


@admin.register(Team)
class TeamAdmin(BaseModelAdmin):
    """
    Admin interface for managing Team records.
    """

    list_display = ("name", "description", "inserted_at")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 30
    readonly_fields = ("inserted_at",)


@admin.register(TeamMembership)
class TeamMembershipAdmin(BaseModelAdmin):
    """
    Admin interface for managing team memberships (user-to-team relationships).
    """

    list_display = ("user", "team", "role", "inserted_at")
    search_fields = ("user__name", "team__name")
    list_filter = ("role", "team__name")
    ordering = ("-inserted_at",)
    readonly_fields = ("inserted_at",)
    list_per_page = 30
