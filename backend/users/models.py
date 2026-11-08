import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class Role(models.TextChoices):
    SEEKER = "SEEKER", "Seeker"
    EMPLOYER = "EMPLOYER", "Employer"
    ADMIN = "ADMIN", "Admin"


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the job portal.

    - Email is the login identifier (no username field).
    - Role drives what the user can see and do across the portal.
    - is_verified gates login: users must confirm their email first.
    - is_active lets admins suspend accounts without deleting them.
    - UUID primary key prevents sequential ID enumeration attacks.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=Role.choices)

    # --- account state ---
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this account is enabled. Unselect instead of deleting accounts",
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Designated whether user has confirmed their email address. Login is blocked until this is True",
    )
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text="Designates whether the user can log into the Django admin site.",
    )

    # --- timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"

    # --- helpers ---

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_seeker(self) -> bool:
        return self.role == Role.SEEKER

    @property
    def is_employer(self) -> bool:
        return self.role == Role.EMPLOYER

    @property
    def is_admin_role(self) -> bool:
        return self.role == Role.ADMIN


class EmailVerificationToken(models.Model):
    """
    Stores a one-time token used to verify a user's email address
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verification_token",
    )
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate a secure random token before saving
        # secrets.token_urlsafe gives a URL-safe base64 string
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def is_expired(self):
        """Token expires after 24 hours"""
        expiry = self.created_at + timedelta(hours=24)
        return timezone.now() > expiry

    def __str__(self):
        return f"VerificationToken for {self.user.email}"
