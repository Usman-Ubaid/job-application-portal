import pytest
from rest_framework.test import APIClient
from companies.models import CompanyProfile
from users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_user():
    def _create_user(role, **kwargs):
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "role": role,
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)

    return _create_user


@pytest.fixture
def create_company():
    def _create_company(user, **kwargs):
        defaults = {
            "company_name": "Solar Financial Services",
            "description": "We are a fintech company.",
            "website": "https://www.sfs.de",
            "user": user,
        }
        defaults.update(kwargs)
        return CompanyProfile.objects.create(**defaults)

    return _create_company


def test_get_my_company(create_user, create_company):
    client = APIClient()
    user = create_user(role="EP")
    create_company(user)
    client.force_authenticate(user=user)
    response = client.get("/api/companies/mine/")
    assert response.status_code == 200
    assert response.data["company_name"] == "Solar Financial Services"


def test_create_company_profile(create_user):
    client = APIClient()
    user = create_user(role="EP")
    client.force_authenticate(user=user)
    response = client.post(
        "/api/companies/mine/",
        {
            "company_name": "Solar Financial Services",
            "description": "We are a fintech company.",
            "website": "https://www.sfs.de",
        },
    )
    company = CompanyProfile.objects.get(company_name="Solar Financial Services")
    assert response.status_code == 201
    assert company.user == user


def test_non_employer_cannot_create_company_profile(create_user):
    client = APIClient()
    user = create_user(role="SK")
    client.force_authenticate(user=user)
    response = client.post(
        "/api/companies/mine/",
        {
            "company_name": "Solar Financial Services",
            "description": "We are a fintech company.",
            "website": "https://www.sfs.de",
            "user": user,
        },
    )
    assert response.status_code == 403


def test_cannot_create_duplicate_company_profile(create_user, create_company):
    client = APIClient()
    user = create_user(role="EP")
    client.force_authenticate(user=user)
    create_company(user)
    response = client.post(
        "/api/companies/mine/",
        {
            "company_name": "Solar Financial Services",
            "description": "We are a fintech company.",
            "website": "https://www.sfs.de",
            "user": user,
        },
    )
    assert response.status_code == 400


def test_patch_company_profile(create_user, create_company):
    client = APIClient()
    user = create_user(role="EP")
    company = create_company(user)
    client.force_authenticate(user=user)
    response = client.patch(
        "/api/companies/mine/",
        {"company_name": "Updated Solar Financial Services"},
    )
    company.refresh_from_db()
    assert response.status_code == 200
    assert company.company_name == "Updated Solar Financial Services"


def test_public_can_view_company_detail(create_user, create_company):
    client = APIClient()
    user = create_user(role="EP")
    company = create_company(user)
    response = client.get(f"/api/companies/{company.id}/")
    assert response.status_code == 200
    assert response.data["company_name"] == "Solar Financial Services"


def test_unauthenticated_user_cannot_access_mine():
    client = APIClient()
    response = client.get("/api/companies/mine/")
    assert response.status_code == 401
