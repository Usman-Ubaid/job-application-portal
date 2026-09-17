from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SEEKER = "SK"
    EMPLOYER = "EP"
    USER_ROLES = [(SEEKER, "Seeker"), (EMPLOYER, "Employer")]
    role = models.CharField(max_length=8, choices=USER_ROLES, default=SEEKER)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
