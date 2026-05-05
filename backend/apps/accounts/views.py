"""
Auth views — register, profile, JWT cookies (optional), email verify, password reset.
"""
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User
from .serializers import (
    PasswordChangeSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    UserSerializer,
)


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    JWT access/refresh ko HttpOnly cookies mein set karta hai (XSS risk kam).
    """

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code != 200:
            return response
        data = response.data
        access = data.get("access")
        refresh = data.get("refresh")
        access_sec = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
        refresh_sec = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
        if access:
            response.set_cookie(
                key="access_token",
                value=access,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=access_sec,
            )
        if refresh:
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=refresh_sec,
            )
        return response


class ThrottledTokenRefreshView(TokenRefreshView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "burst"


class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "burst"

    @staticmethod
    def _send_verification_email(user):
        token = signing.dumps({"uid": user.pk}, salt="email-verify")
        link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        send_mail(
            subject="Verify your email",
            message=f"Link par click karein: {link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        self._send_verification_email(user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "token required"}, status=400)
        try:
            data = signing.loads(token, max_age=60 * 60 * 48, salt="email-verify")
        except signing.BadSignature:
            return Response({"detail": "Invalid token"}, status=400)
        except signing.SignatureExpired:
            return Response({"detail": "Token expired"}, status=400)
        user = User.objects.filter(pk=data.get("uid")).first()
        if not user:
            return Response({"detail": "User not found"}, status=404)
        user.email_verified_at = timezone.now()
        user.save(update_fields=["email_verified_at"])
        return Response({"detail": "Email verified", "user": UserSerializer(user).data})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        ser = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(UserSerializer(request.user).data)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = PasswordChangeSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        if not request.user.check_password(ser.validated_data["old_password"]):
            return Response({"old_password": "Galat password"}, status=400)
        request.user.set_password(ser.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password update ho gaya"})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "burst"

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email__iexact=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            tok = default_token_generator.make_token(user)
            link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={tok}"
            send_mail(
                subject="Password reset",
                message=f"Reset link: {link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        return Response({"detail": "Agar email exist karta hai to mail bhej di gayi."})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        if not all([uid, token, new_password]):
            return Response({"detail": "uid, token, new_password zaroori"}, status=400)
        try:
            validate_password(new_password)
        except Exception as e:  # noqa: BLE001 — validation errors list
            return Response({"new_password": list(e.messages)}, status=400)
        try:
            pk = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=pk)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"detail": "Invalid uid"}, status=400)
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid token"}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password reset ho gaya"})


class GoogleTokenLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "burst"

    def post(self, request):
        try:
            from google.oauth2 import id_token
            from google.auth.transport import requests as google_requests
        except ImportError:
            return Response({"detail": "google-auth install karein"}, status=501)

        token = request.data.get("id_token") or request.data.get("access_token")
        client_id = settings.GOOGLE_OAUTH_CLIENT_ID or request.data.get("client_id")
        if not token or not client_id:
            return Response({"detail": "id_token/access_token aur client_id chahiye"}, status=400)
        try:
            info = id_token.verify_oauth2_token(token, google_requests.Request(), client_id)
        except ValueError:
            return Response({"detail": "Invalid Google token"}, status=400)
        email = info.get("email")
        if not email:
            return Response({"detail": "Email token mein nahi mili"}, status=400)

        user, _created = User.objects.get_or_create(
            email=email.lower(),
            defaults={
                "first_name": info.get("given_name", ""),
                "last_name": info.get("family_name", ""),
            },
        )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )
