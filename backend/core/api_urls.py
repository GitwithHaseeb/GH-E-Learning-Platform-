"""API v1/v2 routing — version namespace sirf documentation ke liye; same views."""
from django.urls import include, path

from core.views import AdminPlatformStatsAPI

urlpatterns = [
    path("admin/platform-stats/", AdminPlatformStatsAPI.as_view(), name="admin-platform-stats"),
    path("", include("apps.accounts.urls")),
    path("", include("apps.courses.urls")),
    path("", include("apps.payments.urls")),
    path("", include("apps.quizzes.urls")),
    path("", include("apps.notifications.urls")),
    path("", include("apps.reviews.urls")),
    path("", include("apps.chat.urls")),
]
