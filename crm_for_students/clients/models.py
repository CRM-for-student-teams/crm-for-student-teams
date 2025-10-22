# Django modules
from django.db import models
from django.conf import settings
from django.utils import timezone

# Project modules
from teams.models import Team, User


class ClientStage(models.Model):
    """
    Represents the various stages a client can be in within the sales or engagement process.

    Stages:
        1 - New
        2 - Contacted
        3 - Negotiating
        4 - Closed (Success)
        5 - Closed (Lost)
    """

    NEW = 1
    CONTACTED = 2
    NEGOTIATING = 3
    CLOSED_SUCCESS = 4
    CLOSED_LOST = 5

    STAGE_CHOICES = [
        (NEW, "New"),
        (CONTACTED, "Contacted"),
        (NEGOTIATING, "Negotiating"),
        (CLOSED_SUCCESS, "Closed (Success)"),
        (CLOSED_LOST, "Closed (Lost)"),
    ]

    status = models.IntegerField(choices=STAGE_CHOICES, unique=True)

    class Meta:
        db_table = "client_stage"
        verbose_name = "Client Stage"
        verbose_name_plural = "Client Stages"


class Client(models.Model):
    """
    Represents a client in the system.
    """

    fullname = models.TextField()
    email = models.CharField(max_length=89, unique=True)
    phone_number = models.TextField()
    stage = models.ForeignKey(
        ClientStage, on_delete=models.SET_NULL, null=True, related_name="clients"
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="clients")

    class Meta:
        db_table = "client"
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class ActivityLog(models.Model):
    """
    Logs actions performed by users on clients.
    """

    action = models.TextField()
    inserted_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activity_logs"
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="activity_logs"
    )

    class Meta:
        db_table = "activity_log"
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
