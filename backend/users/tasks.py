import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retires=3,
    default_retry_delay=60,
)
def send_verification_email_task(self, user_email, user_name, verify_url):
    try:
        send_mail(
            subject="Verify your email address",
            message=(
                f"Hi {user_name},\n\n"
                f"Please verify your email by clicking the link below:\n\n"
                f"{verify_url}\n\n"
                f"This link expires in 24 hours.\n\n"
                f"If you didn't create an account, ignore this email."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,  # raise exception on failure so Celery can catch it
        )
        logger.info(f"Verification email sent to {user_email}")

    except Exception as exc:
        logger.error(f"Failed to send verification email to {user_email}: {exc}")
        raise self.retry(exc=exc)
