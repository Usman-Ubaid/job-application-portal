import pytest
from django.urls import reverse
from rest_framework import status

from users.models import User

from .factories import valid_register_payload

REGISTER_URL = reverse("auth-register")


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def register(api_client, db):
    """
    Wraps POST /auth/register/.

    Including `db` here grants database access to every test that uses
    this fixture — cleaner than marking every test individually.
    """

    def _register(payload):
        return api_client.post(REGISTER_URL, payload, format="json")

    return _register


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


class TestRegisterHappyPath:
    def test_returns_201_on_success(self, register):
        response = register(valid_register_payload())
        assert response.status_code == status.HTTP_201_CREATED

    def test_response_body_shape(self, register):
        """Top-level response must contain 'success', 'message', and 'data'."""
        response = register(valid_register_payload())

        assert "success" in response.data
        assert "message" in response.data
        assert "data" in response.data

    def test_response_data_contains_expected_user_fields(self, register):
        response = register(valid_register_payload())

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

    def test_password_not_in_response(self, register):
        """Security: passwords must never appear in the response."""
        response = register(valid_register_payload())

        assert "password" not in response.data["data"]
        assert "password2" not in response.data["data"]

    def test_user_is_saved_to_database(self, register):
        payload = valid_register_payload()
        register(payload)

        assert User.objects.filter(email=payload["email"]).exists()

    def test_new_user_is_not_verified(self, register):
        """New users must confirm their email before they can log in."""
        payload = valid_register_payload()
        register(payload)

        user = User.objects.get(email=payload["email"])
        assert user.is_verified is False

    def test_seeker_role_is_accepted(self, register):
        response = register(valid_register_payload(role="SEEKER"))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["role"] == "SEEKER"

    def test_employer_role_is_accepted(self, register):
        response = register(valid_register_payload(role="EMPLOYER"))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["role"] == "EMPLOYER"


# ---------------------------------------------------------------------------
# Validation errors
# ---------------------------------------------------------------------------


class TestRegisterValidationErrors:
    """
    All these tests check `response.data["errors"]` — not `response.data` —
    because your API wraps validation errors in an 'errors' envelope.
    """

    def test_duplicate_email_is_rejected(self, register):
        payload = valid_register_payload()
        register(payload)  # first — succeeds
        response = register(payload)  # second — must fail

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data["errors"]  # ← nested under errors

    def test_password_mismatch_is_rejected(self, register):
        payload = valid_register_payload(password2="TotallyDifferent99!")
        response = register(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_short_password_is_rejected(self, register):
        payload = valid_register_payload(password="abc", password2="abc")
        response = register(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data["errors"]

    def test_invalid_email_format_is_rejected(self, register):
        payload = valid_register_payload(email="notanemail")
        response = register(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data["errors"]

    def test_missing_email_is_rejected(self, register):
        payload = valid_register_payload()
        del payload["email"]
        response = register(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data["errors"]

    def test_missing_first_name_is_rejected(self, register):
        payload = valid_register_payload()
        del payload["first_name"]
        response = register(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "first_name" in response.data["errors"]

    def test_missing_last_name_is_rejected(self, register):
        payload = valid_register_payload()
        del payload["last_name"]
        response = register(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "last_name" in response.data["errors"]

    def test_missing_role_is_rejected(self, register):
        payload = valid_register_payload()
        del payload["role"]
        response = register(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "role" in response.data["errors"]

    def test_invalid_role_is_rejected(self, register):
        payload = valid_register_payload(role="HACKER")
        response = register(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "role" in response.data["errors"]


# ---------------------------------------------------------------------------
# Business rules
# ---------------------------------------------------------------------------


class TestRegisterBusinessRules:
    def test_admin_role_registration_is_blocked(self, register):
        payload = valid_register_payload(role="ADMIN")
        response = register(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "role" in response.data["errors"]

    def test_admin_user_is_not_saved_to_db(self, register):
        payload = valid_register_payload(role="ADMIN")
        register(payload)

        assert not User.objects.filter(email=payload["email"], role="ADMIN").exists()


# ---------------------------------------------------------------------------
# HTTP contract
# ---------------------------------------------------------------------------


class TestRegisterHttpContract:
    def test_get_is_not_allowed(self, api_client):
        response = api_client.get(REGISTER_URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_is_not_allowed(self, api_client):
        response = api_client.put(REGISTER_URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_empty_body_is_rejected(self, register):
        response = register({})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
