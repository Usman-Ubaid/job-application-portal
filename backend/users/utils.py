from .models import EmailVerificationToken
from .tasks import send_verification_email_task


def send_verification_email(user, request):
    """
    Creates a verification tooken for the user and sends them an email.
    """

    EmailVerificationToken.objects.filter(user=user).delete()

    token_obj = EmailVerificationToken.objects.create(user=user, token="")

    verify_url = request.build_absolute_uri(
        f"/api/users/verify-email/?token={token_obj}"
    )

    send_verification_email_task.delay(
        user_email=user.email,
        user_name=user.first_name or user.email,
        verify_url=verify_url,
    )
