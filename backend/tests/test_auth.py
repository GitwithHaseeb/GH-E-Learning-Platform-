import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User, UserRole


@pytest.mark.django_db
def test_register_and_me():
    c = APIClient()
    r = c.post(
        "/api/v1/auth/register/",
        {
            "email": "stu@test.com",
            "password": "Testpass123!",
            "password_confirm": "Testpass123!",
            "role": UserRole.STUDENT,
        },
        format="json",
    )
    assert r.status_code == 201
    access = r.data["access"]
    c.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    me = c.get("/api/v1/users/me/")
    assert me.status_code == 200
    assert me.data["email"] == "stu@test.com"
