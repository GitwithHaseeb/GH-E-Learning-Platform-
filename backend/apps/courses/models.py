"""
Courses, lessons, enrollments, progress, bookmarks, notes, announcements.
"""
import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Multi-level: parent null = root category."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, db_index=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("name",)
        indexes = [models.Index(fields=["parent", "slug"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:130]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class CourseLevel(models.TextChoices):
    BEGINNER = "beginner", "Beginner"
    INTERMEDIATE = "intermediate", "Intermediate"
    EXPERT = "expert", "Expert"
    MASTER = "master", "Master"


class PricingType(models.TextChoices):
    FREE = "free", "Free"
    PAID = "paid", "Paid"


class CourseStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PENDING = "pending", "Pending approval"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class Course(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    learning_outcomes = models.JSONField(default=list, help_text="What you'll learn bullet points")
    related_topics = models.JSONField(default=list, help_text="Related topic chips")
    requirements = models.JSONField(default=list, help_text="Course requirements list")
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses_teaching",
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="courses")
    tags = models.ManyToManyField(Tag, blank=True, related_name="courses")
    level = models.CharField(max_length=20, choices=CourseLevel.choices, default=CourseLevel.BEGINNER)
    pricing = models.CharField(max_length=10, choices=PricingType.choices, default=PricingType.FREE)
    price_cents = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=0, help_text="Approx total video/content minutes")
    duration_months = models.PositiveSmallIntegerField(default=1)
    thumbnail = models.ImageField(upload_to="courses/thumbnails/", blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, help_text="External image URL for catalog cards")
    promo_video = models.FileField(upload_to="courses/promo/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=CourseStatus.choices, default=CourseStatus.DRAFT)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    ratings_count = models.PositiveIntegerField(default=0)
    enrollments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status", "pricing"]),
            models.Index(fields=["-average_rating"]),
            models.Index(fields=["-enrollments_count"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:210]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class LessonType(models.TextChoices):
    VIDEO = "video", "Video"
    PDF = "pdf", "PDF"
    ARTICLE = "article", "Article"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0, db_index=True)
    lesson_type = models.CharField(max_length=20, choices=LessonType.choices, default=LessonType.VIDEO)
    video_file = models.FileField(upload_to="lessons/video/", blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="Cloudinary/S3/CDN URL agar file upload nahi")
    pdf_file = models.FileField(upload_to="lessons/pdf/", blank=True, null=True)
    article_content = models.TextField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="unlocks",
        help_text="Pehle yeh lessons complete hone chahiye",
    )

    class Meta:
        ordering = ("course", "order", "id")
        indexes = [
            models.Index(fields=["course", "order"]),
        ]

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    last_lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    progress_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "course")
        indexes = [models.Index(fields=["user", "-enrolled_at"])]

    def __str__(self):
        return f"{self.user.email} → {self.course.title}"


class LessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress_records")
    completed = models.BooleanField(default=False)
    last_position_seconds = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "lesson")
        indexes = [models.Index(fields=["user", "lesson"])]

    def __str__(self):
        return f"{self.user_id}:{self.lesson_id}"


class LessonBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lesson")


class LessonNote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_notes")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="notes")
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user", "lesson"])]


class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="announcements")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)


class Certificate(models.Model):
    """Course complete hone par PDF certificate (Celery task generate karti hai)."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificates")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="certificates")
    code = models.CharField(max_length=40, unique=True, db_index=True)
    pdf_file = models.FileField(upload_to="certificates/", blank=True, null=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        ordering = ("-issued_at",)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4()).replace("-", "")[:12]
        super().save(*args, **kwargs)


class CoursePhase(models.Model):
    """Each course has 5 structured learning phases."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="phases")
    phase_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    resources = models.JSONField(default=list, help_text="List of reading resources: [{title, url}]")

    class Meta:
        ordering = ("course", "phase_number")
        unique_together = ("course", "phase_number")

    def __str__(self):
        return f"{self.course.title} · Phase {self.phase_number}"


class CoursePhaseQuiz(models.Model):
    """30 MCQs for each phase."""

    phase = models.OneToOneField(CoursePhase, on_delete=models.CASCADE, related_name="quiz")
    questions = models.JSONField(default=list, help_text="List of 30: {question, options[4], answer_index}")
    pass_mark_percent = models.PositiveSmallIntegerField(default=60)


class CoursePhaseProgress(models.Model):
    """User progress per phase + quick quiz result."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="phase_progress")
    phase = models.ForeignKey(CoursePhase, on_delete=models.CASCADE, related_name="progress_records")
    reading_completed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    quiz_score_percent = models.PositiveSmallIntegerField(default=0)
    attempts = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "phase")
