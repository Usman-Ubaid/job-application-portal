from django.db import models
from django.conf import settings


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
