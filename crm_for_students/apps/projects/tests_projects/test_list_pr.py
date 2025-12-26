from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)


def test_project_list(auth_client_student_captain) -> None:
    """Good: Authenticated user can list projects"""
    response: Response = auth_client_student_captain.get("/api/projects/")
    assert response.status_code == HTTP_200_OK


def test_project_list_unauthenticated(api_client) -> None:
    """Bad: Unauthenticated user cannot list projects"""
    response: Response = api_client.get("/api/projects/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_project_list_invalid_method(auth_client_student_captain) -> None:
    """Bad: Invalid method (POST not allowed)"""
    response: Response = auth_client_student_captain.post("/api/projects/")
    assert response.status_code in (HTTP_400_BAD_REQUEST, 405)


def test_project_list_forbidden(auth_client_student_member) -> None:
    """Bad: Access forbidden for user without permission (simulate with wrong role)"""
    response: Response = auth_client_student_member.get("/api/projects/")
    assert response.status_code in (HTTP_401_UNAUTHORIZED, 403)
