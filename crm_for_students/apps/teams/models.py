# Python modules
from typing import Any

# Django modules
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import(
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to make database requests
    """
    def __obtain_user_instance(
        self,
        email: str,
        full_name: str,
        password: str, 
        **kwargs: dict[str, Any],
    ):
        if not email:
            raise ValidationError(
                message="Email field is required"
            )
        new_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password,
            full_name=full_name,
            **kwargs,
        )
        return new_user
    
    def create_user(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ):
        new_user = self.__obtain_user_instance(
            email=email,
            password=password,
            full_name=full_name,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user
    
    def create_superuser(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ):
        new_superuser = self.__obtain_user_instance(
            email=email,
            full_name=full_name,
            password=password,
            **{
                "is_staff": True,
                "is_superuser": True,
            **kwargs,
            },
        )
        new_superuser.set_password(password)
        new_superuser.save(using=self._db)
        return new_superuser


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user in the system.
    """

    ROLE_CHOICES = [
        ("student_captain", "Student Captain"),
        ("student_member", "Student Member"),
        ("client", "Client"),

    ]

    ROLE_MAX_LENGHT = 50
    EMAIL_MAX_LENGHT = 150
    PASSWORD_MAX_LENGHT = 200
    FULLNAME_MAX_LENGHT = 240

    email = models.EmailField(max_length=EMAIL_MAX_LENGHT, unique=True)
    password = models.CharField(max_length=200, validators=[validate_password])
    full_name = models.CharField(max_length=FULLNAME_MAX_LENGHT)
    role = models.CharField(max_length=ROLE_MAX_LENGHT, choices=ROLE_CHOICES)
    inserted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]
    objects = CustomUserManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return f"{self.email}"


class Team(models.Model):
    """
    Represents a team within the system.
    """
    NAME_MAX_LENGHT = 200

    name = models.CharField(max_length=NAME_MAX_LENGHT)
    description = models.TextField()
    inserted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="TeamMembership", related_name="teams", verbose_name="members"
    )

    class Meta:
        db_table = "team"
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self) -> str:
        return f"{self.name}"


class TeamMembership(models.Model):
    """
    Intermediate model for linking users to teams with a specific role.
    """

    ROLE_CHOICES = [
        ("captain", "Captain"),
        ("member", "Member"),
    ]
    ROLE_MAX_LENGHT = 50

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=ROLE_MAX_LENGHT, choices=ROLE_CHOICES)
    inserted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "team_membership"
        verbose_name = "Team membership"
        verbose_name_plural = "Teams membership"

    def __str__(self) -> str:
        return f"{self.user.full_name} -> {self.team.name} (role: {self.role})"
