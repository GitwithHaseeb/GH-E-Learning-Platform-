from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from . import views

urlpatterns = [
    path("auth/register/", views.RegisterView.as_view(), name="auth-register"),
    path("auth/login/", views.CookieTokenObtainPairView.as_view(), name="auth-login"),
    path("auth/token/refresh/", views.ThrottledTokenRefreshView.as_view(), name="auth-refresh"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="auth-logout"),
    path("auth/verify-email/", views.VerifyEmailView.as_view(), name="auth-verify-email"),
    path("auth/password/reset/", views.PasswordResetRequestView.as_view(), name="auth-password-reset"),
    path("auth/password/reset/confirm/", views.PasswordResetConfirmView.as_view(), name="auth-password-reset-confirm"),
    path("auth/social/google/", views.GoogleTokenLoginView.as_view(), name="auth-google"),
    path("users/me/", views.MeView.as_view(), name="users-me"),
    path("users/me/password/", views.PasswordChangeView.as_view(), name="users-password"),
]
