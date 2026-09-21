import pytest
from rest_framework.test import APIClient
from users.models import User

pytestmark = pytest.mark.django_db


def test_user_can_register():
    client = APIClient()
    response = client.post(
        "/api/auth/register/",
        {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password2": "testpass123",
            "role": "SK",
        },
    )

    user = User.objects.get(email="test@example.com")
    assert response.status_code == 201
    assert User.objects.filter(email="test@example.com").exists()
    assert user.check_password("testpass123")


def test_user_cannot_register_with_mismatch_passwords():
    client = APIClient()
    response = client.post(
        "/api/auth/register/",
        {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password2": "testpass121",
            "role": "SK",
        },
    )

    assert response.status_code == 400


def test_user_cannot_register_with_duplicate_email():
    client = APIClient()
    client.post(
        "/api/auth/register/",
        {
            "username": "testuser1",
            "email": "test@example.com",
            "password": "testpass123",
            "password2": "testpass123",
            "role": "SK",
        },
    )

    response = client.post(
        "/api/auth/register/",
        {
            "username": "testuser2",
            "email": "test@example.com",
            "password": "testpass123",
            "password2": "testpass123",
            "role": "SK",
        },
    )

    assert response.status_code == 400
    assert "email" in response.data


def test_user_cannot_register_without_email():
    client = APIClient()
    response = client.post(
        "/api/auth/register/",
        {
            "username": "testuser2",
            "password": "testpass123",
            "password2": "testpass121",
            "role": "SK",
        },
    )

    assert response.status_code == 400


def test_user_cannot_register_with_invalid_email():
    client = APIClient()
    response = client.post(
        "/api/auth/register/",
        {
            "username": "testuser2",
            "email": "test@example",
            "password": "testpass123",
            "password2": "testpass123",
            "role": "SK",
        },
    )

    assert response.status_code == 400
