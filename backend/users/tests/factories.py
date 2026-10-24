# backend/users/tests/factories.py

"""
Raw request payload builders — plain Python dicts, no database involved.

These are used to construct the data you POST to the API.
conftest.py handles actual database object creation separately.
"""


def valid_register_payload(**overrides) -> dict:
    """
    Returns a valid registration payload for POST /auth/register/.

    Usage:
        valid_register_payload()                            # all defaults
        valid_register_payload(email="other@test.com")     # override email
        valid_register_payload(role="EMPLOYER")            # test employer path
    """
    payload = {
        "email": "jane.doe@example.com",
        "first_name": "Jane",
        "last_name": "Doe",
        "password": "SecurePass123!",
        "password2": "SecurePass123!",
        "role": "SEEKER",
    }
    payload.update(overrides)
    return payload


def valid_login_payload(**overrides) -> dict:
    """
    Returns a valid login payload for POST /auth/login/.

    The email and password match the defaults used by the `create_user`
    fixture in conftest.py, so they work together out of the box.

    Usage:
        valid_login_payload()                            # all defaults
        valid_login_payload(email="other@test.com")     # override email
        valid_login_payload(password="WrongPass!")      # test bad password
    """
    payload = {
        "email": "test@example.com",  # matches create_user default
        "password": "SecurePass123!",  # matches create_user default
    }
    payload.update(overrides)
    return payload
