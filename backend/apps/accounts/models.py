"""
Custom User model — roles Student / Instructor / Admin.
Email hi login identifier hai (username field nahi).
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserRole(models.TextChoices):
    STUDENT = "student", "Student"
    INSTRUCTOR = "instructor", "Instructor"
    ADMIN = "admin", "Admin"


class UserManager(BaseUserManager):
    """User.objects.create_user / create_superuser helpers."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email zaroori hai")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.ADMIN)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser ke liye is_staff=True hona chahiye")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser ke liye is_superuser=True hona chahiye")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        ordering = ("-date_joined",)
        indexes = [
            models.Index(fields=["role", "is_active"]),
        ]

    def __str__(self):
        return self.email

    @property
    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT

    @property
    def is_instructor(self) -> bool:
        return self.role == UserRole.INSTRUCTOR

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN or self.is_superuser
