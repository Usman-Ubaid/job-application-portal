from rest_framework.permissions import BasePermission
from users.models import Role


class IsEmployer(BasePermission):
    """Grants access only to users with the EMPLOYER role."""

    message = "Only employers can perform this action."

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and request.user.role == Role.EMPLOYER


class isAdminRole(BasePermission):
    """Grants access only to users with the ADMIN role."""

    message = "Only admins can perform this action"

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and request.user.role == Role.ADMIN


class IsSeeker(BasePermission):
    """Grants access only to users with the SEEKER role."""

    message = "Only job seekers can perform this action."

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and request.user.role == Role.SEEKER
