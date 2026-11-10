from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import EmailVerificationToken
from .serializers import RegisterSerializer, UserSerializer
from .utils import send_verification_email

User = get_user_model()


class RegisterView(APIView):
    """
    POST /auth/register/
    Creates a new user account and returns the user payload.
    The account is inactive until the email is verified.
    """

    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                user = serializer.save()
                user.is_verified = False
                user.save(update_fields=["is_verified"])

                send_verification_email(user, request)

        except Exception:
            return Response(
                {
                    "success": False,
                    "message": "Registration Failed. Please try again later.",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                "success": "True",
                "message": "Account created. Please check your email to verify your account.",
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """
    POST /auth/login/
    Authenticates the user.
    Returns access + refresh JWT token alongside user info.
    Blocked for unverified users.
    """

    permission_classes = (AllowAny,)

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        data = response.data

        access_token = data.pop("access")
        refresh_token = data.pop("refresh")

        response = Response(
            {"success": True, "message": "Login successful.", "data": response.data},
            status=status.HTTP_200_OK,
        )

        # Set tokens as HttpOnly cookies instead
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=60 * 15,  # 15 minutes
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=60 * 60 * 24 * 7,  # 7 days
        )

        return response


class LogoutView(APIView):
    """
    POST /auth/logout/
    Blacklists the refresh token, effectively ending the session.
    The short-lived access token will expire on its own.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"success": False, "message": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"success": False, "message": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = Response(
            {"success": True, "message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class CookieTokenRefreshView(APIView):
    """
    POST auth/token/refresh/
    Reads refresh token from cookie, returns a new access token as a cookie.
    """

    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"success": False, "message": "No refresh token found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
        except TokenError:
            return Response(
                {"success": False, "message": "Invalid or expired refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {"success": True, "message": "Token refreshed."},
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=60 * 15,
        )
        return response


class MeView(APIView):
    """
    GET /auth/me/
    Returns the currently authenticated user's profile
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        return Response(
            {
                "success": True,
                "data": UserSerializer(request.user).data,
            },
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(APIView):
    """
    GET /api/users/verify-email/?token=<token>
    """

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        token_value = request.query_params.get("token")

        if not token_value:
            return Response(
                {"success": False, "message": "No token provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token_obj = EmailVerificationToken.objects.select_related("user").get(
                token=token_value
            )

        except EmailVerificationToken.DoesNotExist:
            return Response(
                {"success": False, "message": "Invalid or already used token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if token_obj.is_expired():
            token_obj.delete()
            return Response(
                {
                    "success": False,
                    "message": "Token has expired. Please register again or request a new link",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = token_obj.user
        user.is_verified = True
        user.save(update_fields=["is_verified"])

        token_obj.delete()

        return Response(
            {
                "success": True,
                "message": "Email verified successfully. You can now log in",
            },
            status=status.HTTP_200_OK,
        )
