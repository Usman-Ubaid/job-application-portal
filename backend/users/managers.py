from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the User model where email is the unique
    identifier for authentication instead of username.
    """

    def _create_user(self, email: str, password: str, **extra_fields) -> "User":
        """
        Core helper that both create_user and create_superuser delegate to.
        Validates, normalises and persists a user.
        """
        if not email:
            raise ValueError("An email address is required")

        if not password:
            raise ValueError("A password is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields) -> "User":
        """
        Creates a regular user (SEEKER or EMPLOYER).
        - is_staff      → False  (no admin panel access)
        - is_superuser  → False  (no blanket permissions)
        - is_verified   → False  (must confirm email)
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_verified", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        """
        Creates a superuser via `python manage.py createsuperuser`.
        Only used by developers / ops — never called from the API.
        - is_staff      → True
        - is_superuser  → True
        - is_verified   → True  (operator controls the email directly)
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
