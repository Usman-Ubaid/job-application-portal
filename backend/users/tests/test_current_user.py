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


def test_get_current_user(create_user):
    user = create_user(
        username="testuser",
        email="test@example.com",
        role="SK",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/auth/user/")

    assert response.status_code == 200
    assert response.data["id"] == user.id
    assert response.data["username"] == "testuser"
    assert response.data["email"] == "test@example.com"
    assert response.data["role"] == "SK"


def test_unauthenticated_user_cannot_get_current_user():
    client = APIClient()

    response = client.get("/api/auth/user/")

    assert response.status_code == 401
