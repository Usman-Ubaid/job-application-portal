import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
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

    assert response.status_code == 201


@pytest.mark.django_db
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


@pytest.mark.django_db
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
            "password2": "testpass121",
            "role": "SK",
        },
    )

    assert response.status_code == 400
