from django.db import models
from django.conf import settings


class JobPosting(models.Model):
    FULL_TIME = "FT"
    PART_TIME = "PT"
    CONTRACT = "C"
    INTERNSHIP = "I"
    EMPLOYMENT_TYPE = [
        (FULL_TIME, "Full_time"),
        (PART_TIME, "Part_time"),
        (CONTRACT, "Contract"),
        (INTERNSHIP, "Internship"),
    ]
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    description = models.TextField()
    location = models.CharField(max_length=60, blank=True, null=True)
    salary_range = models.CharField(max_length=50, blank=True, null=True)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
