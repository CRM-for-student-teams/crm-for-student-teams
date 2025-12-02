# Pytest modules
import pytest
# Django modules
from django.contrib.auth import get_user_model
# DRF modules
from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED,
)
# Project modules
from apps.teams.models import Team, TeamMembership

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="testuser@example.com",
        password="TestPassword123!",
        full_name="Test User"
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        email="anotheruser@example.com",
        password="TestPassword123!",
        full_name="Another User",
    )


@pytest.fixture
def team(db):
    return Team.objects.create(
        name="Test Team",
        description="This is a test team"
    )


@pytest.mark.django_db
class TestUserRegistration:

    def test_register_new_user_successfully(self, api_client):
        url = "/api/auth/register/"
        data = {
            "email": "newuser@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "full_name": "New User"
        }
        response = api_client.post(url, data)
        assert response.status_code == HTTP_201_CREATED

    def test_register_with_different_passwords(self, api_client):
        url = "/api/auth/register/"
        data = {
            "email": "newuser@example.com",
            "password": "Password123",
            "password_confirm": "DifferentPassword123",
            "full_name": "New User"
        }
        response = api_client.post(url, data)
        assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:

    def test_login_with_correct_info(self, api_client, user):
        url = "/api/auth/login/"
        data = {"email": "testuser@example.com",
                "password": "TestPassword123!"}
        response = api_client.post(url, data)
        assert response.status_code == HTTP_200_OK

    def test_login_with_wrong_info(self, api_client, user):
        url = "/api/auth/login/"
        data = {"email": "testuser@example.com",
                "password": "WrongPassword123"}
        response = api_client.post(url, data)
        assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCurrentUser:

    def test_get_current_user_when_login(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = "/api/auth/me/"
        response = api_client.get(url)
        assert response.status_code == HTTP_200_OK

    def test_get_current_user_when_not_login(self, api_client):
        url = "/api/auth/me/"
        response = api_client.get(url)
        assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCreateTeam:

    def test_create_team_successfully(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = "/api/teams/"
        data = {"name": "My New Team", "description": "This is description"}
        response = api_client.post(url, data)
        assert response.status_code == HTTP_201_CREATED

    def test_create_team_without_login(self, api_client):
        url = "/api/teams/"
        data = {"name": "My Team", "description": "Description"}
        response = api_client.post(url, data)
        assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUpdateTeam:

    def test_update_team_captain(self, api_client, user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_captain")
        url = f"/api/teams/{team.id}/"
        data = {"name": "Updated Team Name",
                "description": "Updated description"}
        response = api_client.put(url, data)
        assert response.status_code == HTTP_200_OK

    def test_update_team_member(self, api_client, user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_member")
        url = f"/api/teams/{team.id}/"
        data = {"name": "Trying to Update", "description": "New description"}
        response = api_client.put(url, data)
        assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDeleteTeam:

    def test_delete_team_captain(self, api_client, user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_captain")
        url = f"/api/teams/{team.id}/"
        response = api_client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_delete_team_member(self, api_client, user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_member")
        url = f"/api/teams/{team.id}/"
        response = api_client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestLeaveTeam:

    def test_member_can_leave_team(self, api_client, user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_member")
        url = f"/api/teams/{team.id}/leave_team/"
        response = api_client.post(url)
        assert response.status_code == HTTP_200_OK

    def test_captain_cant_leave_team(self, api_client, user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_captain")
        url = f"/api/teams/{team.id}/leave_team/"
        response = api_client.post(url)
        assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAddTeamMember:

    def test_captain_can_add_member(self, api_client, user, another_user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_captain")
        url = "/api/membership/"
        data = {"team": team.id, "user_id": another_user.id,
                "role": "student_member"}
        response = api_client.post(url, data)
        assert response.status_code == HTTP_201_CREATED

    def test_member_cant_add_member(self, api_client, user, another_user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_member")
        url = "/api/membership/"
        data = {"team": team.id, "user_id": another_user.id,
                "role": "student_member"}
        response = api_client.post(url, data)
        assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestRemoveTeamMember:

    def test_captain_can_remove_member(self, api_client, user, another_user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_captain")
        membership = TeamMembership.objects.create(
            team=team, user=another_user, role="student_member")
        url = f"/api/membership/{membership.id}/"
        response = api_client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_member_cant_remove_member(self, api_client, user, another_user, team):
        api_client.force_authenticate(user=user)
        TeamMembership.objects.create(
            team=team, user=user, role="student_member")
        membership = TeamMembership.objects.create(
            team=team, user=another_user, role="student_member")
        url = f"/api/membership/{membership.id}/"
        response = api_client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN
