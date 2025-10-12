#django modules
from django.db import models
from django.conf import settings 
from django.utils import timezone


class ClientStage(models.Model):
    NEW = 1
    CONTACTED = 2
    NEGOTIATING = 3
    CLOSED_SUCCESS = 4
    CLOSED_LOST = 5

    STAGE_CHOICES = [
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (NEGOTIATING, 'Negotiating'),
        (CLOSED_SUCCESS, 'Closed (Success)'),
        (CLOSED_LOST, 'Closed (Lost)'),
    ]

    status = models.IntegerField(choices=STAGE_CHOICES, unique=True)

    class Meta:
        db_table = "client_stage"   
        verbose_name = "Client Stage"
        verbose_name_plural = "Client Stages"

class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True)
    inserted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "teams"  # custom table name
        verbose_name = "Team"
        verbose_name_plural = "Teams"

class Client(models.Model):
    fullname = models.TextField()
    email = models.CharField(max_length=89, unique=True)
    phone_number = models.TextField()
    stage = models.ForeignKey(
        ClientStage,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='clients'
    )

    class Meta:
        db_table = "client"  
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class ActivityLog(models.Model):
    action = models.TextField()
    inserted_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    class Meta:
        db_table = "activity_log"
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"