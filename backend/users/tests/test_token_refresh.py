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


def test_valid_new_refresh_token(create_user):
    client = APIClient()
    user = create_user()
    login_response = client.post(
        "/api/auth/login/", {"email": "test@example.com", "password": "testpass123"}
    )
    old_refresh_value = login_response.cookies.get("refresh_token").value
    old_access_value = login_response.cookies.get("access_token").value

    response = client.post("/api/auth/token/refresh/")

    new_refresh_value = response.cookies.get("refresh_token").value
    new_access_value = response.cookies.get("access_token").value

    assert old_refresh_value != new_refresh_value
    assert new_access_value != old_access_value
    assert response.status_code == 200


def test_no_refresh_token_provided():
    client = APIClient()
    response = client.post("/api/auth/token/refresh/")
    assert response.status_code == 401


def test_invalid_refresh_token():
    client = APIClient()
    client.cookies["refresh_token"] = "garbage.invalid.token"
    response = client.post("/api/auth/token/refresh/")
    assert response.status_code == 401


def test_blacklisted_refresh_token_cannot_be_reused(create_user):
    client = APIClient()
    create_user()
    login_response = client.post(
        "/api/auth/login/", {"email": "test@example.com", "password": "testpass123"}
    )
    old_refresh_value = login_response.cookies.get("refresh_token").value

    first_refresh_response = client.post("/api/auth/token/refresh/")
    assert first_refresh_response.status_code == 200

    # Manually set the cookie back to the original (now blacklisted) refresh token
    client.cookies["refresh_token"] = old_refresh_value
    second_refresh_response = client.post("/api/auth/token/refresh/")

    assert second_refresh_response.status_code == 401
