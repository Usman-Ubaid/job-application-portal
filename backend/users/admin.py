from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin panel configuration for the User model.
    Replaces username with email in all admin views.
    """

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_verified",
        "is_active",
        "created_at",
    )
    list_filter = ("role", "is_verified", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": ("id", "email", "password"),
            },
        ),
        (
            "Personal info",
            {
                "fields": ("first_name", "last_name", "role"),
            },
        ),
        (
            "Account state",
            {
                "fields": ("is_active", "is_verified", "is_staff", "is_superuser"),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("groups", "user_permissions"),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
