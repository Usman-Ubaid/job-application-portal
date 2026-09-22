import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from applications.models import Application
from jobs.models import JobPosting
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
def create_job():
    def _create_job(user, **kwargs):
        defaults = {
            "title": "Senior Software Engineer",
            "description": "At least 5 years of experience",
            "location": "Berlin, Germany",
            "salary_range": "90,000 - 120,000",
            "employment_type": "FT",
            "employer": user,
            "is_active": True,
        }
        defaults.update(kwargs)
        return JobPosting.objects.create(**defaults)

    return _create_job


@pytest.fixture
def cv_file():
    return SimpleUploadedFile("cv.pdf", b"file_content", content_type="application/pdf")


@pytest.fixture
def create_application():
    def _create_application(job, applicant, **kwargs):
        defaults = {
            "job": job,
            "applicant": applicant,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "cv": SimpleUploadedFile(
                "cv.pdf", b"file_content", content_type="application/pdf"
            ),
        }
        defaults.update(kwargs)
        return Application.objects.create(**defaults)

    return _create_application


def test_seeker_can_apply_to_job(create_user, create_job, cv_file):
    employer = create_user(role="EP")
    seeker = create_user(role="SK", username="seeker1", email="seeker@example.com")
    job = create_job(employer)
    client = APIClient()
    client.force_authenticate(user=seeker)

    response = client.post(
        f"/api/jobs/{job.id}/apply/",
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "cv": cv_file,
        },
        format="multipart",
    )

    assert response.status_code == 201
    assert Application.objects.filter(job=job, applicant=seeker).exists()


def test_employer_cannot_apply_to_job(create_user, create_job, cv_file):
    employer = create_user(role="EP")
    job = create_job(employer)
    client = APIClient()
    client.force_authenticate(user=employer)

    response = client.post(
        f"/api/jobs/{job.id}/apply/",
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "cv": cv_file,
        },
        format="multipart",
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_apply(create_user, create_job, cv_file):
    employer = create_user(role="EP")
    job = create_job(employer)
    client = APIClient()

    response = client.post(
        f"/api/jobs/{job.id}/apply/",
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "cv": cv_file,
        },
        format="multipart",
    )

    assert response.status_code == 401


def test_cannot_apply_to_inactive_job(create_user, create_job, cv_file):
    employer = create_user(role="EP")
    seeker = create_user(role="SK", username="seeker1", email="seeker@example.com")
    job = create_job(employer, is_active=False)
    client = APIClient()
    client.force_authenticate(user=seeker)

    response = client.post(
        f"/api/jobs/{job.id}/apply/",
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "cv": cv_file,
        },
        format="multipart",
    )

    assert response.status_code == 400


def test_cannot_apply_twice_to_same_job(
    create_user, create_job, create_application, cv_file
):
    employer = create_user(role="EP")
    seeker = create_user(role="SK", username="seeker1", email="seeker@example.com")
    job = create_job(employer)
    create_application(job, seeker)
    client = APIClient()
    client.force_authenticate(user=seeker)

    response = client.post(
        f"/api/jobs/{job.id}/apply/",
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "cv": cv_file,
        },
        format="multipart",
    )

    assert response.status_code == 400


def test_employer_can_view_applicants(create_user, create_job, create_application):
    employer = create_user(role="EP")
    seeker = create_user(role="SK", username="seeker1", email="seeker@example.com")
    job = create_job(employer)
    create_application(job, seeker)
    client = APIClient()
    client.force_authenticate(user=employer)

    response = client.get(f"/api/jobs/{job.id}/applicants/")

    assert response.status_code == 200
    assert len(response.data) == 1


def test_non_owner_employer_cannot_view_applicants(
    create_user, create_job, create_application
):
    employer1 = create_user(role="EP")
    employer2 = create_user(
        role="EP", username="employer2", email="employer2@example.com"
    )
    seeker = create_user(role="SK", username="seeker1", email="seeker@example.com")
    job = create_job(employer1)
    create_application(job, seeker)
    client = APIClient()
    client.force_authenticate(user=employer2)

    response = client.get(f"/api/jobs/{job.id}/applicants/")

    assert response.status_code == 403


def test_seeker_can_view_own_applications(create_user, create_job, create_application):
    employer = create_user(role="EP")
    seeker = create_user(role="SK", username="seeker1", email="seeker@example.com")
    job = create_job(employer)
    create_application(job, seeker)
    client = APIClient()
    client.force_authenticate(user=seeker)

    response = client.get("/api/applications/mine/")

    assert response.status_code == 200
    assert len(response.data) == 1


def test_seeker_only_sees_own_applications(create_user, create_job, create_application):
    employer = create_user(role="EP")
    seeker1 = create_user(role="SK", username="seeker1", email="seeker1@example.com")
    seeker2 = create_user(role="SK", username="seeker2", email="seeker2@example.com")
    job = create_job(employer)
    create_application(job, seeker1)
    client = APIClient()
    client.force_authenticate(user=seeker2)

    response = client.get("/api/applications/mine/")

    assert response.status_code == 200
    assert len(response.data) == 0


def test_employer_can_update_application_status(
    create_user, create_job, create_application
):
    employer = create_user(role="EP")
    seeker = create_user(role="SK", username="seeker1", email="seeker@example.com")
    job = create_job(employer)
    application = create_application(job, seeker)
    client = APIClient()
    client.force_authenticate(user=employer)

    response = client.patch(
        f"/api/applications/{application.id}/",
        {"status": "REV"},
    )
    application.refresh_from_db()

    assert response.status_code == 200
    assert application.status == "REV"


def test_non_owner_employer_cannot_update_status(
    create_user, create_job, create_application
):
    employer1 = create_user(role="EP")
    employer2 = create_user(
        role="EP", username="employer2", email="employer2@example.com"
    )
    seeker = create_user(role="SK", username="seeker1", email="seeker@example.com")
    job = create_job(employer1)
    application = create_application(job, seeker)
    client = APIClient()
    client.force_authenticate(user=employer2)

    response = client.patch(
        f"/api/applications/{application.id}/",
        {"status": "REV"},
    )
    application.refresh_from_db()

    assert response.status_code == 403
    assert application.status == "S"


def test_seeker_cannot_update_application_status(
    create_user, create_job, create_application
):
    employer = create_user(role="EP")
    seeker = create_user(role="SK", username="seeker1", email="seeker@example.com")
    job = create_job(employer)
    application = create_application(job, seeker)
    client = APIClient()
    client.force_authenticate(user=seeker)

    response = client.patch(
        f"/api/applications/{application.id}/",
        {"status": "REV"},
    )

    assert response.status_code == 403
