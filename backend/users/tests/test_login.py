# backend/users/tests/test_login.py

import pytest
from django.urls import reverse
from rest_framework import status

from .factories import valid_login_payload

# Module-level constant — same pattern as REGISTER_URL in test_register.py.
# reverse() is safe to call at import time for stable named URLs.
LOGIN_URL = reverse("auth-login")


# --------------------------------------------------------------------------- #
#  Shared fixture                                                               #
# --------------------------------------------------------------------------- #


@pytest.fixture
def login(api_client, db):
    """
    Wraps POST /auth/login/.

    Declaring `db` here grants database access to every test that uses
    this fixture — the same pattern as the `register` fixture.
    This means we don't need @pytest.mark.django_db on any test class.
    """

    def _login(payload):
        return api_client.post(LOGIN_URL, payload, format="json")

    return _login


# --------------------------------------------------------------------------- #
#  Happy path                                                                   #
# --------------------------------------------------------------------------- #


class TestLoginHappyPath:
    def test_returns_200_on_success(self, login, seeker):
        """
        `seeker` is a verified user from conftest.py.
        valid_login_payload() uses the same email/password as the seeker
        fixture defaults, so no overrides needed.
        """
        response = login(valid_login_payload())

        assert response.status_code == status.HTTP_200_OK

    def test_response_body_shape(self, login, seeker):
        """Top-level response must contain 'success', 'message', and 'data'."""
        response = login(valid_login_payload())

        assert "success" in response.data
        assert "message" in response.data
        assert "data" in response.data

    def test_response_success_and_message_values(self, login, seeker):
        """The envelope values themselves must be correct, not just present."""
        response = login(valid_login_payload())

        assert response.data["success"] is True
        assert response.data["message"] == "Login successful."

    def test_response_data_contains_user_info(self, login, seeker):
        """
        User info is nested inside 'data'. We assert against the seeker
        fixture's actual field values — not hardcoded strings — so if
        conftest defaults change, this test adapts automatically.
        """
        response = login(valid_login_payload())
        user_data = response.data["data"]["user"]

        assert user_data["email"] == seeker.email
        assert user_data["first_name"] == seeker.first_name
        assert user_data["last_name"] == seeker.last_name

    def test_tokens_set_as_httponly_cookies(self, login, seeker):
        """
        Tokens must live in HttpOnly cookies, not the response body.
        HttpOnly = JavaScript cannot read this cookie, which blocks
        XSS attacks from stealing tokens.
        """
        response = login(valid_login_payload())

        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies
        assert response.cookies["access_token"]["httponly"] is True
        assert response.cookies["refresh_token"]["httponly"] is True

    def test_tokens_absent_from_response_body(self, login, seeker):
        """
        Raw token strings must never appear in the JSON body.
        If they did, any JS on the page could read them — defeating
        the entire point of using HttpOnly cookies.
        """
        response = login(valid_login_payload())
        body = response.data

        assert "access" not in body
        assert "refresh" not in body
        assert "access" not in body.get("data", {})
        assert "refresh" not in body.get("data", {})


# --------------------------------------------------------------------------- #
#  Blocked: unverified user                                                     #
# --------------------------------------------------------------------------- #


class TestLoginUnverifiedUser:
    def test_unverified_user_is_blocked(self, login, create_user):
        """
        We use create_user() with is_verified=False rather than the `seeker`
        fixture because seeker is always verified. We want to override just
        that one field — this is exactly what create_user() is designed for.
        """
        create_user(email="unverified@example.com", is_verified=False)
        response = login(valid_login_payload(email="unverified@example.com"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unverified_user_gets_descriptive_error(self, login, create_user):
        """
        A vague 'invalid credentials' error here would confuse users who
        simply forgot to check their inbox. The message from AuthenticationFailed
        in your serializer must tell them exactly why they're blocked.
        """
        create_user(email="unverified@example.com", is_verified=False)
        response = login(valid_login_payload(email="unverified@example.com"))

        assert "verify your email" in str(response.data).lower()

    def test_unverified_user_receives_no_cookies(self, login, create_user):
        """
        A blocked login must not set any cookies at all — not even partially.
        Leaking a token on a failed login would be a serious auth bug.
        """
        create_user(email="unverified@example.com", is_verified=False)
        response = login(valid_login_payload(email="unverified@example.com"))

        assert "access_token" not in response.cookies
        assert "refresh_token" not in response.cookies


# --------------------------------------------------------------------------- #
#  Validation errors                                                            #
# --------------------------------------------------------------------------- #


class TestLoginValidationErrors:
    """
    These tests check that malformed input is caught at the serializer
    level before authentication even runs — hence 400, not 401.

    400 = the request itself is malformed (client mistake).
    401 = request was valid but credentials were rejected (auth failure).
    """

    def test_missing_email_returns_400(self, login):
        payload = valid_login_payload()
        del payload["email"]
        response = login(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_password_returns_400(self, login):
        payload = valid_login_payload()
        del payload["password"]
        response = login(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_body_returns_400(self, login):
        response = login({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# --------------------------------------------------------------------------- #
#  Wrong credentials                                                            #
# --------------------------------------------------------------------------- #


class TestLoginWrongCredentials:
    def test_wrong_password_is_rejected(self, login, seeker):
        """
        Correct email, wrong password. We override just the password —
        this is exactly what the override pattern in valid_login_payload() is for.
        """
        response = login(valid_login_payload(password="TotallyWrongPassword!"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_nonexistent_email_returns_401(self, login):
        """
        Must return 401, not 404. Returning 404 would reveal whether an
        email is registered — that's an account enumeration vulnerability.
        Always return the same error regardless of whether the email exists.

        No db fixture needed — we intentionally want this email absent from the DB.
        """
        response = login(valid_login_payload(email="ghost@example.com"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# --------------------------------------------------------------------------- #
#  Business rules                                                               #
# --------------------------------------------------------------------------- #


class TestLoginBusinessRules:
    def test_inactive_user_is_blocked(self, login, create_user):
        """
        Django's ModelBackend automatically rejects is_active=False users.
        We verify that gate is still in place and hasn't been accidentally bypassed.
        """
        create_user(email="inactive@example.com", is_active=False)
        response = login(valid_login_payload(email="inactive@example.com"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_inactive_user_receives_no_cookies(self, login, create_user):
        """A suspended account must not receive any tokens."""
        create_user(email="inactive@example.com", is_active=False)
        response = login(valid_login_payload(email="inactive@example.com"))

        assert "access_token" not in response.cookies
        assert "refresh_token" not in response.cookies


# --------------------------------------------------------------------------- #
#  HTTP contract                                                                #
# --------------------------------------------------------------------------- #


class TestLoginHttpContract:
    def test_get_is_not_allowed(self, api_client):
        """
        Login is POST-only. GET must return 405 Method Not Allowed.
        GET requests must never trigger auth side-effects.
        No db access needed — rejected before any auth logic runs.
        """
        response = api_client.get(LOGIN_URL)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_is_not_allowed(self, api_client):
        response = api_client.put(LOGIN_URL)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
