from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    CookieTokenRefreshView,
    MeView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="auth-token-refresh"),
    path("user/", MeView.as_view(), name="auth-me"),
]
