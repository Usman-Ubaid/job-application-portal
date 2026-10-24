import pytest
from django.urls import reverse
from rest_framework import status

ME_URL = reverse("auth-me")


# --------------------------------------------------------------------------- #
#  Shared fixture                                                               #
# --------------------------------------------------------------------------- #


@pytest.fixture
def me(authenticated_client, db):
    """
    Wraps GET /auth/me/.

    Uses `authenticated_client` from conftest.py — a client that already
    has the seeker user force-authenticated. This is appropriate here
    because MeView only checks IsAuthenticated; it doesn't inspect
    JWT cookies, so force_authenticate() is sufficient and simpler.
    """

    def _me():
        return authenticated_client.get(ME_URL, format="json")

    return _me


# --------------------------------------------------------------------------- #
#  Happy path                                                                   #
# --------------------------------------------------------------------------- #


class TestMeHappyPath:
    def test_returns_200_for_authenticated_user(self, me):
        response = me()

        assert response.status_code == status.HTTP_200_OK

    def test_response_body_shape(self, me):
        """Top-level response must contain 'success' and 'data'."""
        response = me()

        assert "success" in response.data
        assert "data" in response.data

    def test_response_success_value(self, me):
        response = me()

        assert response.data["success"] is True

    def test_response_data_contains_expected_user_fields(self, me):
        """
        The fields returned must match what UserSerializer exposes.
        We pin these explicitly so that if someone adds or removes a
        field from the serializer, this test catches it immediately.
        """
        response = me()

        expected_fields = {
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "is_verified",
            "created_at",
        }
        assert set(response.data["data"].keys()) == expected_fields

    def test_returns_correct_user_data(self, me, seeker):
        """
        The data returned must belong to the authenticated user —
        not a default, not another user. We assert against the seeker
        fixture's actual values so if conftest defaults change, this
        test adapts automatically.
        """
        response = me()
        data = response.data["data"]

        assert data["email"] == seeker.email
        assert data["first_name"] == seeker.first_name
        assert data["last_name"] == seeker.last_name
        assert data["role"] == seeker.role
        assert data["full_name"] == seeker.full_name

    def test_password_not_in_response(self, me):
        """
        Security: password must never appear in the response.
        This is the same guard we apply on register — worth checking
        on every endpoint that returns user data.
        """
        response = me()

        assert "password" not in response.data["data"]

    def test_is_verified_reflects_actual_user_state(self, me, seeker):
        """
        The seeker fixture is verified by default (is_verified=True).
        We confirm the serializer is reading the real field value
        rather than hardcoding or defaulting it.
        """
        response = me()

        assert response.data["data"]["is_verified"] == seeker.is_verified


# --------------------------------------------------------------------------- #
#  Authentication                                                               #
# --------------------------------------------------------------------------- #


class TestMeAuthentication:
    def test_unauthenticated_request_returns_401(self, api_client, db):
        """
        IsAuthenticated must block requests with no credentials.
        We use a plain api_client with no force_authenticate() call.
        """
        response = api_client.get(ME_URL, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_each_user_sees_only_their_own_data(self, api_client, create_user, db):
        """
        Two different users must each get back their own profile.
        This guards against a bug where request.user is ignored and
        a hardcoded or cached user is returned instead.

        This is a subtle but real class of bug — worth an explicit test.
        """
        user_a = create_user(email="user_a@example.com")
        user_b = create_user(email="user_b@example.com")

        # Authenticate as user A and call /me/
        api_client.force_authenticate(user=user_a)
        response_a = api_client.get(ME_URL, format="json")

        # Re-authenticate as user B and call /me/
        api_client.force_authenticate(user=user_b)
        response_b = api_client.get(ME_URL, format="json")

        assert response_a.data["data"]["email"] == user_a.email
        assert response_b.data["data"]["email"] == user_b.email

        # Cross-check: neither response contains the other user's email
        assert response_a.data["data"]["email"] != user_b.email
        assert response_b.data["data"]["email"] != user_a.email


# --------------------------------------------------------------------------- #
#  HTTP contract                                                                #
# --------------------------------------------------------------------------- #


class TestMeHttpContract:
    def test_post_is_not_allowed(self, authenticated_client):
        response = authenticated_client.post(ME_URL, format="json")

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_is_not_allowed(self, authenticated_client):
        response = authenticated_client.put(ME_URL, format="json")

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
