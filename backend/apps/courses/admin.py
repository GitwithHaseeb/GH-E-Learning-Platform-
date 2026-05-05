from django.contrib import admin

from .models import (
    Announcement,
    Category,
    Certificate,
    Course,
    CoursePhase,
    CoursePhaseProgress,
    CoursePhaseQuiz,
    Enrollment,
    Lesson,
    LessonBookmark,
    LessonNote,
    LessonProgress,
    Tag,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor", "status", "pricing", "price_cents", "average_rating", "enrollments_count")
    list_filter = ("status", "pricing", "level")
    search_fields = ("title", "instructor__email")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "lesson_type")
    list_filter = ("lesson_type",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "progress_percent", "enrolled_at")


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed", "last_position_seconds")


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "author", "created_at")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "code", "issued_at")


@admin.register(CoursePhase)
class CoursePhaseAdmin(admin.ModelAdmin):
    list_display = ("course", "phase_number", "title")
    list_filter = ("phase_number",)


@admin.register(CoursePhaseQuiz)
class CoursePhaseQuizAdmin(admin.ModelAdmin):
    list_display = ("phase", "pass_mark_percent")


@admin.register(CoursePhaseProgress)
class CoursePhaseProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "phase", "completed", "quiz_score_percent", "attempts", "updated_at")
