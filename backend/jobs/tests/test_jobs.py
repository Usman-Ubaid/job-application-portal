import pytest
from rest_framework.test import APIClient
from jobs.models import JobPosting
from users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "role": "SK",
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


def test_get_all_jobs(create_user, create_job):
    employer = create_user(role="EP")
    client = APIClient()
    create_job(employer)
    response = client.get("/api/jobs/")
    assert response.status_code == 200
    assert response.data[0]["title"] == "Senior Software Engineer"


def test_get_all_active_jobs(create_user, create_job):
    employer = create_user(role="EP")
    client = APIClient()
    create_job(employer)
    create_job(employer)
    create_job(employer, is_active=False)
    response = client.get("/api/jobs/")
    assert response.status_code == 200
    assert len(response.data) == 2
    assert all(job["is_active"] for job in response.data)


def test_create_job(create_user):
    client = APIClient()
    employer = create_user(role="EP")
    client.force_authenticate(user=employer)
    response = client.post(
        "/api/jobs/",
        {
            "title": "Senior Software Engineer",
            "description": "At least 5 years of experience",
            "location": "Berlin, Germany",
            "salary_range": "90,000 - 120,000",
            "employment_type": "FT",
            "is_active": True,
        },
    )
    job = JobPosting.objects.get(title="Senior Software Engineer")

    assert job.employer == employer
    assert response.status_code == 201


def test_non_employer_cannot_create_job(create_user):
    user = create_user(role="SK")

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/jobs/",
        {
            "title": "Senior Software Engineer",
            "description": "At least 5 years of experience",
            "location": "Berlin, Germany",
            "salary_range": "90,000 - 120,000",
            "employment_type": "FT",
            "is_active": True,
        },
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_create_job():
    client = APIClient()
    response = client.post(
        "/api/jobs/",
        {
            "title": "Senior Software Engineer",
            "description": "At least 5 years of experience",
            "location": "Berlin, Germany",
            "salary_range": "90,000 - 120,000",
            "employment_type": "FT",
            "is_active": True,
        },
    )

    assert response.status_code == 401


def test_get_job(create_user, create_job):
    employer = create_user(role="EP")
    client = APIClient()
    client.force_authenticate(user=employer)
    job = create_job(employer)

    response = client.get(f"/api/jobs/{job.id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Senior Software Engineer"


def test_unauthenticated_user_can_get_job(create_user, create_job):
    employer = create_user(role="EP")
    client = APIClient()

    job = create_job(employer)

    response = client.get(f"/api/jobs/{job.id}/")

    assert response.status_code == 200
    assert response.data["title"] == "Senior Software Engineer"


def test_get_job_id_does_not_exist(create_user, create_job):
    employer = create_user(role="EP")
    client = APIClient()
    job = create_job(employer)
    response = client.get("/api/jobs/999/")
    assert response.status_code == 404


def test_delete_job(create_user, create_job):
    employer = create_user(role="EP")
    client = APIClient()
    client.force_authenticate(user=employer)
    job = create_job(employer)

    response = client.delete(f"/api/jobs/{job.id}/")
    assert response.status_code == 204
    assert not JobPosting.objects.filter(id=job.id).exists()


def test_non_owner_cannot_delete_job(create_user, create_job):
    employer1 = create_user(role="EP")
    employer2 = create_user(username="testuser1", email="test2@example.com", role="EP")
    client = APIClient()
    client.force_authenticate(user=employer2)
    job = create_job(employer1)

    response = client.delete(f"/api/jobs/{job.id}/")
    assert response.status_code == 403
    assert JobPosting.objects.filter(id=job.id).exists()


def test_unauthenticated_user_cannot_delete_job(create_user, create_job):
    employer = create_user(role="EP")
    client = APIClient()
    job = create_job(employer)

    response = client.delete(f"/api/jobs/{job.id}/")
    assert response.status_code == 401
    assert JobPosting.objects.filter(id=job.id).exists()


def test_delete_job_id_does_not_exist():
    client = APIClient()

    response = client.delete("/api/jobs/999/")

    assert response.status_code == 404


def test_patch_own_job(create_user, create_job):
    employer = create_user(role="EP")
    client = APIClient()
    client.force_authenticate(user=employer)
    job = create_job(employer)

    response = client.patch(
        f"/api/jobs/{job.id}/",
        {
            "title": "Junior Full Stack Developer",
        },
    )
    get_job = JobPosting.objects.get(id=job.id)
    assert response.status_code == 200
    assert get_job.title == "Junior Full Stack Developer"


def test_non_owner_cannot_patch_job(create_user, create_job):
    employer1 = create_user(role="EP")
    employer2 = create_user(username="testuser1", email="test2@example.com", role="EP")
    client = APIClient()
    client.force_authenticate(user=employer1)
    job = create_job(employer2)

    response = client.patch(
        f"/api/jobs/{job.id}/",
        {
            "title": "Junior Full Stack Developer",
        },
    )
    job.refresh_from_db()
    assert response.status_code == 403
    assert job.title == "Senior Software Engineer"


def test_unauthenticated_user_cannot_patch_job(create_user, create_job):
    employer = create_user(role="EP")
    client = APIClient()
    job = create_job(employer)

    response = client.patch(
        f"/api/jobs/{job.id}/",
        {
            "title": "Junior Full Stack Developer",
        },
    )
    job.refresh_from_db()
    assert response.status_code == 401
    assert job.title == "Senior Software Engineer"


def test_patch_job_id_does_not_exist():
    client = APIClient()

    response = client.patch(
        "/api/jobs/999/",
        {"title": "Junior Full Stack Developer"},
    )

    assert response.status_code == 404
