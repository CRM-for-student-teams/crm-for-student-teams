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

    def __str__(self):
        return dict(self.STAGE_CHOICES)[self.status]

class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True)
    inserted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

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