# backend/users/tests/test_logout.py

import pytest
from django.urls import reverse
from rest_framework import status

LOGOUT_URL = reverse("auth-logout")
LOGIN_URL = reverse("auth-login")


# --------------------------------------------------------------------------- #
#  Shared fixture                                                               #
# --------------------------------------------------------------------------- #


@pytest.fixture
def logout(logged_in_client, db):
    """
    Wraps POST /auth/logout/.

    Uses `logged_in_client` instead of plain `api_client` because logout
    requires both:
      1. IsAuthenticated to pass (handled by force_authenticate in the fixture)
      2. A real refresh_token cookie to exist (planted by the login POST)

    `db` here grants database access to every test that uses this fixture,
    following the same pattern as the `login` and `register` fixtures.
    """

    def _logout():
        return logged_in_client.post(LOGOUT_URL, format="json")

    return _logout


# --------------------------------------------------------------------------- #
#  Happy path                                                                   #
# --------------------------------------------------------------------------- #


class TestLogoutHappyPath:
    def test_returns_200_on_success(self, logout):
        response = logout()

        assert response.status_code == status.HTTP_200_OK

    def test_response_body_shape(self, logout):
        """Top-level response must contain 'success' and 'message'."""
        response = logout()

        assert "success" in response.data
        assert "message" in response.data

    def test_response_success_and_message_values(self, logout):
        """The envelope values themselves must be correct, not just present."""
        response = logout()

        assert response.data["success"] is True
        assert response.data["message"] == "Logged out successfully."

    def test_access_token_cookie_is_cleared(self, logout):
        """
        After logout, the access_token cookie must be deleted.
        delete_cookie() sets the cookie with an empty value and
        a past expiry date — the browser then discards it.
        We check the value is empty as the signal it's been cleared.
        """
        response = logout()

        assert response.cookies["access_token"].value == ""

    def test_refresh_token_cookie_is_cleared(self, logout):
        """Same as above for the refresh_token cookie."""
        response = logout()

        assert response.cookies["refresh_token"].value == ""


# --------------------------------------------------------------------------- #
#  Token blacklist                                                              #
# --------------------------------------------------------------------------- #


class TestLogoutTokenBlacklist:
    """
    These tests verify the most important security property of logout:
    the refresh token must actually be invalidated server-side, not just
    cleared from the browser. If blacklisting fails silently, a stolen
    refresh token would still work after the user logs out.
    """

    def test_blacklisted_token_cannot_be_used_to_refresh(
        self, logged_in_client, api_client, seeker, db
    ):
        """
        Full flow:
          1. Log in → get refresh token cookie
          2. Log out → token is blacklisted
          3. Try to use the same token to get a new access token → must fail

        This is the most important logout test. It proves the session is
        actually ended server-side, not just cleared from the browser.
        """
        refresh_url = reverse("auth-token-refresh")

        # Capture the refresh token before logout clears it
        refresh_token_value = logged_in_client.cookies.get("refresh_token")

        # Log out — this blacklists the token
        logged_in_client.post(LOGOUT_URL, format="json")

        # Now try to use the blacklisted token on a fresh client
        # (simulates an attacker who captured the token before logout)
        api_client.cookies["refresh_token"] = refresh_token_value
        response = api_client.post(refresh_url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_twice_returns_400(self, logged_in_client, db):
        """
        Logging out a second time with the same (now blacklisted) token
        must fail with 400. This also proves the first logout actually
        blacklisted the token — a double logout is an implicit blacklist check.
        """
        logged_in_client.post(LOGOUT_URL, format="json")  # first — succeeds
        response = logged_in_client.post(
            LOGOUT_URL, format="json"
        )  # second — must fail

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# --------------------------------------------------------------------------- #
#  Business rules                                                               #
# --------------------------------------------------------------------------- #


class TestLogoutBusinessRules:
    def test_missing_refresh_cookie_returns_400(self, api_client, seeker, db):
        """
        If the refresh_token cookie is absent (e.g. already cleared,
        or the request came from an unusual client), return 400.
        We authenticate the user but deliberately don't set the cookie.
        """
        api_client.force_authenticate(user=seeker)
        response = api_client.post(LOGOUT_URL, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_refresh_cookie_error_message(self, api_client, seeker, db):
        """The error message must explain what's missing."""
        api_client.force_authenticate(user=seeker)
        response = api_client.post(LOGOUT_URL, format="json")

        assert response.data["success"] is False
        assert response.data["message"] == "Refresh token is required."

    def test_invalid_token_returns_400(self, api_client, seeker, db):
        """
        A malformed or tampered token string must be caught by the
        TokenError handler in the view and return 400.
        """
        api_client.force_authenticate(user=seeker)
        api_client.cookies["refresh_token"] = "this.is.not.a.valid.jwt"
        response = api_client.post(LOGOUT_URL, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_token_error_message(self, api_client, seeker, db):
        """The error message must reflect that the token itself is bad."""
        api_client.force_authenticate(user=seeker)
        api_client.cookies["refresh_token"] = "this.is.not.a.valid.jwt"
        response = api_client.post(LOGOUT_URL, format="json")

        assert response.data["success"] is False
        assert response.data["message"] == "Invalid or expired token."


# --------------------------------------------------------------------------- #
#  Authentication                                                               #
# --------------------------------------------------------------------------- #


class TestLogoutAuthentication:
    def test_unauthenticated_request_returns_401(self, api_client, db):
        """
        LogoutView has IsAuthenticated as its permission class.
        A request with no credentials at all must be blocked before
        any logout logic runs.
        """
        response = api_client.post(LOGOUT_URL, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# --------------------------------------------------------------------------- #
#  HTTP contract                                                                #
# --------------------------------------------------------------------------- #


class TestLogoutHttpContract:
    def test_get_is_not_allowed(self, authenticated_client):
        """
        We use authenticated_client here — not plain api_client.
        IsAuthenticated runs before the method check, so an unauthenticated
        request returns 401 before Django even checks the HTTP method.
        """
        response = authenticated_client.get(LOGOUT_URL)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_is_not_allowed(self, authenticated_client):
        response = authenticated_client.put(LOGOUT_URL)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
