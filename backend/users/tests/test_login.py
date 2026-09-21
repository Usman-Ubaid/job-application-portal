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


def test_login_with_correct_credentials(create_user):
    create_user()
    client = APIClient()

    response = client.post(
        "/api/auth/login/", {"email": "test@example.com", "password": "testpass123"}
    )

    assert response.status_code == 200


def test_login_with_incorrect_credentials(create_user):
    create_user()
    client = APIClient()

    response = client.post(
        "/api/auth/login/", {"email": "test@example.com", "password": "testpass125"}
    )

    assert response.status_code == 401


def test_login_with_nonexistent_email(create_user):
    create_user()
    client = APIClient()

    response = client.post(
        "/api/auth/login/", {"email": "test@example.de", "password": "testpass123"}
    )

    assert response.status_code == 404


def test_login_sets_cookies(create_user):
    create_user()
    client = APIClient()

    response = client.post(
        "/api/auth/login/", {"email": "test@example.com", "password": "testpass123"}
    )
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    assert response.status_code == 200


def test_login_without_password(create_user):
    create_user()

    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {"email": "test@example.com"},
    )

    assert response.status_code == 400
