# Third party modules
from rest_framework.test import APITestCase
from rest_framework import status

# Django modules
from django.urls import reverse

# Local modules
from .models import CustomUser


class UserCRUDTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            full_name="Test User",
            password="initial123",
            role="student_member"
        )

    def test_create_user(self):
        url = reverse("user-create")
        data = {
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "password123",
            "role": "student_member"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(
            email="newuser@example.com").full_name, "New User")

    def test_read_user(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_user(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        data = {
            "full_name": "Updated Name",
            "password": "newpassword123"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, "Updated Name")
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_delete_user(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())
