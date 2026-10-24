# backend/users/tests/conftest.py

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import Role, User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def _create_user(**overrides):
        defaults = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass123!",
            "role": Role.SEEKER,
            "is_verified": True,
        }
        defaults.update(overrides)
        return User.objects.create_user(**defaults)

    return _create_user


@pytest.fixture
def seeker(create_user):
    return create_user()


@pytest.fixture
def employer(create_user):
    return create_user(
        email="employer@example.com",
        role=Role.EMPLOYER,
    )


@pytest.fixture
def authenticated_client(api_client, seeker):
    api_client.force_authenticate(user=seeker)
    return api_client


@pytest.fixture
def logged_in_client(api_client, seeker):
    """
    Returns an APIClient that has been through a real login flow.

    Why do this instead of force_authenticate()?
    force_authenticate() bypasses JWT entirely — it's useful for testing
    protected endpoints, but for logout we specifically need a real
    refresh token cookie to exist on the client. Only an actual login
    POST produces one.
    """
    login_url = reverse("auth-login")
    response = api_client.post(
        login_url,
        {"email": seeker.email, "password": "SecurePass123!"},
        format="json",
    )

    # Extract the refresh token from the login response cookie
    # and plant it on the client so subsequent requests carry it.
    refresh_token = response.cookies.get("refresh_token")
    access_token = response.cookies.get("access_token")

    if refresh_token:
        api_client.cookies["refresh_token"] = refresh_token.value
    if access_token:
        api_client.cookies["access_token"] = access_token.value

    # Also authenticate the client so IsAuthenticated passes
    api_client.force_authenticate(user=seeker)

    return api_client
