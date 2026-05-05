from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Course, Enrollment
from apps.payments.models import Order, OrderStatus

from core.permissions import IsAdmin

User = get_user_model()


class AdminPlatformStatsAPI(APIView):
    """High-level counts — admin dashboard ke liye."""

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response(
            {
                "users": User.objects.count(),
                "courses": Course.objects.count(),
                "enrollments": Enrollment.objects.count(),
                "paid_orders": Order.objects.filter(status=OrderStatus.PAID).count(),
            }
        )
