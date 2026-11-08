from django.conf import settings
from django.core.mail import send_mail

from .models import EmailVerificationToken


def send_verification_email(user, request):
    """
    Creates a verification tooken for the user and sends them an email.
    """

    EmailVerificationToken.objects.filter(user=user).delete()

    token_obj = EmailVerificationToken.objects.create(user=user, token="")

    verify_url = request.build_absolute_uri(
        f"/api/v1/auth/verify-email/?token={token_obj}"
    )

    send_mail(
        subject="Verify your email address",
        message=(
            f"Hi {user.first_name or user.email},\n\n"
            f"Please verify your email by clicking the link below:\n\n"
            f"{verify_url}\n\n"
            f"This link expires in 24 hours.\n\n"
            f"If you didn't create an account, ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
