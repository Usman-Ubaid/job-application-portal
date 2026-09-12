from django.db import models
from django.conf import settings
from jobs.models import JobPosting


class Application(models.Model):
    SUBMITTED = "S"
    REVIEWED = "REV"
    REJECTED = "REJ"
    ACCEPTED = "A"
    STATUS = [
        (SUBMITTED, "submitted"),
        (REVIEWED, "reviewed"),
        (REJECTED, "rejected"),
        (ACCEPTED, "accepted"),
    ]
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="applications", on_delete=models.CASCADE
    )
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=3, choices=STATUS, default=SUBMITTED)
    applied_at = models.DateTimeField(auto_now_add=True)
