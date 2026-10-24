import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

TOKEN_REFRESH_URL = reverse("auth-token-refresh")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def set_refresh_cookie(client, user):
    """
    Generates a real refresh token for the given user and attaches it
    to the test client's cookies — exactly as the login view would do.

    We do this directly instead of calling the login endpoint so that
    token refresh tests are independent of login working correctly.
    """
    refresh = RefreshToken.for_user(user)
    client.cookies["refresh_token"] = str(refresh)
    return refresh


# ---------------------------------------------------------------------------
# Success cases
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestTokenRefreshSuccess:
    def test_returns_200_with_valid_refresh_token(self, api_client, seeker):
        """A valid refresh token cookie should return 200."""
        set_refresh_cookie(api_client, seeker)
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert response.status_code == status.HTTP_200_OK

    def test_response_body_shape(self, api_client, seeker):
        """Response should contain 'success' and 'message' keys."""
        set_refresh_cookie(api_client, seeker)
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert "success" in response.data
        assert "message" in response.data

    def test_access_token_cookie_is_set(self, api_client, seeker):
        """
        The new access token should arrive as a cookie named 'access_token',
        not in the response body. This is the core contract of this endpoint.
        """
        set_refresh_cookie(api_client, seeker)
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert "access_token" in response.cookies

    def test_access_token_cookie_is_httponly(self, api_client, seeker):
        """
        HttpOnly means JavaScript cannot read this cookie.
        This is a security requirement — we verify it explicitly.
        """
        set_refresh_cookie(api_client, seeker)
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert response.cookies["access_token"]["httponly"] is True

    def test_access_token_is_not_in_response_body(self, api_client, seeker):
        """
        Tokens must never appear in the response body — only in cookies.
        If they're in the body, JavaScript can read them (XSS risk).
        """
        set_refresh_cookie(api_client, seeker)
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert "access_token" not in response.data


# ---------------------------------------------------------------------------
# Missing token
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestTokenRefreshMissingToken:
    def test_returns_401_when_no_cookie_present(self, api_client):
        """
        No cookie at all — the view checks request.COOKIES.get("refresh_token")
        and returns 401 if it's missing.
        """
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_error_message_when_no_cookie(self, api_client):
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert response.data["success"] is False
        assert response.data["message"] == "No refresh token found."

    def test_no_access_token_cookie_set_on_failure(self, api_client):
        """When the request fails, no access_token cookie should be set."""
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert "access_token" not in response.cookies


# ---------------------------------------------------------------------------
# Invalid / expired token
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestTokenRefreshInvalidToken:
    def test_returns_401_with_invalid_token(self, api_client):
        """
        A malformed string is not a valid JWT — simplejwt raises TokenError,
        which the view catches and returns 401.
        """
        api_client.cookies["refresh_token"] = "this.is.not.a.valid.token"
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_error_message_with_invalid_token(self, api_client):
        api_client.cookies["refresh_token"] = "this.is.not.a.valid.token"
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert response.data["success"] is False
        assert response.data["message"] == "Invalid or expired refresh token."

    def test_returns_401_with_blacklisted_token(self, api_client, seeker):
        """
        Once a refresh token is blacklisted (e.g. after logout), it must
        not be usable again. simplejwt raises TokenError for blacklisted tokens,
        so the view should return 401.

        Note: this test only works if 'rest_framework_simplejwt.token_blacklist'
        is in your INSTALLED_APPS. If blacklisting isn't set up yet, skip this
        with @pytest.mark.skip(reason="token blacklist not configured").
        """
        refresh = RefreshToken.for_user(seeker)
        api_client.cookies["refresh_token"] = str(refresh)

        # Blacklist the token — simulates what logout does
        refresh.blacklist()

        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_no_access_token_cookie_set_on_invalid_token(self, api_client):
        """No access_token cookie should be set when the token is invalid."""
        api_client.cookies["refresh_token"] = "bad.token.here"
        response = api_client.post(TOKEN_REFRESH_URL, format="json")

        assert "access_token" not in response.cookies


# ---------------------------------------------------------------------------
# HTTP contract
# ---------------------------------------------------------------------------


class TestTokenRefreshHttpContract:
    def test_get_is_not_allowed(self, api_client):
        response = api_client.get(TOKEN_REFRESH_URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_is_not_allowed(self, api_client):
        response = api_client.put(TOKEN_REFRESH_URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
