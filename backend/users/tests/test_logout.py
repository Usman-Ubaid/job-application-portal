import pytest
from rest_framework.test import APIClient
from users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "role": "SK",
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)

    return _create_user


def test_authenticated_user_can_logout(create_user):
    create_user()
    client = APIClient()
    login_response = client.post(
        "/api/auth/login/", {"email": "test@example.com", "password": "testpass123"}
    )
    response = client.post("/api/auth/logout/")

    assert response.status_code == 200
    assert response.cookies["access_token"].value == ""
    assert response.cookies["refresh_token"].value == ""


def test_unauthenticated_user_cannot_logout():
    client = APIClient()
    response = client.post("/api/auth/logout/")
    assert response.status_code == 401
