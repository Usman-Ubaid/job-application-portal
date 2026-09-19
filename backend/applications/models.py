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
    COVER_LETTER_FILE = "CLF"
    COVER_LETTER_TEXT = "CLT"
    COVER_LETTERS = [
        (COVER_LETTER_FILE, "cover_letter_file"),
        (COVER_LETTER_TEXT, "cover_letter_text"),
    ]
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cv = models.FileField(upload_to="cvs/", null=True, blank=True)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True, null=True)
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="applications", on_delete=models.CASCADE
    )
    cover_letter_text = models.TextField(blank=True, null=True)
    cover_letter_file = models.FileField(
        blank=True, null=True, upload_to="cover_letters/"
    )
    cover_letter_type = models.CharField(
        max_length=3,
        choices=COVER_LETTERS,
        default=COVER_LETTER_TEXT,
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=3, choices=STATUS, default=SUBMITTED)
    applied_at = models.DateTimeField(auto_now_add=True)
