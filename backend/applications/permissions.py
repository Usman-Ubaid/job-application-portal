from rest_framework.permissions import BasePermission
from users.models import User


class IsSeeker(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.SEEKER
