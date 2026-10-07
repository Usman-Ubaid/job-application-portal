from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from .models import Role

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles new user registration.
    - Validates password strength via Django's AUTH_PASSWORD_VALIDATORS.
    - Prevents ADMIN self-registration (admins are created via CLI only).
    """

    password = serializers.CharField(
        write_only=True, min_length=8, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password", "password2", "role")

    def validate_role(self, value: str) -> str:
        """Block self-registration as ADMIN"""
        if value == Role.ADMIN:
            raise serializers.ValidationError("You cannot register with the admin role")
        return value

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs.pop("password"):
            raise serializers.ValidationError({"password": "Passwords do no match"})

        return attrs

    def create(self, validated_data: dict):
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends the Simple JWT's default login serializer to:
    1. Block unverified users with a clear error message.
    2. Embed basic user info in the token response.
    """

    def validate(self, attr: dict) -> dict:
        data = super().validate(attr)
        user = self.user

        if not user.is_verified:
            raise AuthenticationFailed(
                "Please verify your email address before signing in."
            )

        data["user"] = UserSerializer(user).data
        return data


class UserSerializer(serializers.ModelSerializer):
    """Read-only representation of a user - safe to return in API response"""

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "is_verified",
            "created_at",
        )
        read_only_fields = fields
