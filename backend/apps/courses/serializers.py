from django.db.models import Avg
from rest_framework import serializers

from apps.reviews.models import CourseReview

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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent", "description", "children")

    def get_children(self, obj):
        qs = obj.children.all()[:20]
        return CategorySerializer(qs, many=True).data


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "order",
            "lesson_type",
            "duration_seconds",
            "is_preview",
        )


class LessonDetailSerializer(serializers.ModelSerializer):
    prerequisites = LessonListSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "course",
            "title",
            "order",
            "lesson_type",
            "video_file",
            "video_url",
            "pdf_file",
            "article_content",
            "duration_seconds",
            "is_preview",
            "prerequisites",
        )


class LessonWriteSerializer(serializers.ModelSerializer):
    prerequisites = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Lesson.objects.all(), required=False
    )

    class Meta:
        model = Lesson
        fields = (
            "course",
            "title",
            "order",
            "lesson_type",
            "video_file",
            "video_url",
            "pdf_file",
            "article_content",
            "duration_seconds",
            "is_preview",
            "prerequisites",
        )

    def validate(self, attrs):
        course = attrs.get("course") or getattr(self.instance, "course", None)
        pre = attrs.get("prerequisites", None)
        if pre is not None and course:
            for p in pre:
                if p.course_id != course.id:
                    raise serializers.ValidationError("Prerequisite lesson same course ka hona chahiye.")
        return attrs


class CourseListSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)
    display_image = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "slug",
            "subtitle",
            "learning_outcomes",
            "related_topics",
            "requirements",
            "instructor_name",
            "category",
            "category_name",
            "level",
            "pricing",
            "price_cents",
            "duration_minutes",
            "duration_months",
            "thumbnail",
            "thumbnail_url",
            "display_image",
            "average_rating",
            "ratings_count",
            "enrollments_count",
            "status",
        )

    def get_instructor_name(self, obj):
        u = obj.instructor
        return f"{u.first_name} {u.last_name}".strip() or u.email

    def get_display_image(self, obj):
        if obj.thumbnail:
            try:
                return obj.thumbnail.url
            except Exception:
                pass
        return obj.thumbnail_url


class CourseDetailSerializer(CourseListSerializer):
    tags = TagSerializer(many=True, read_only=True)
    lessons = LessonListSerializer(many=True, read_only=True)
    phases = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + (
            "description",
            "promo_video",
            "tags",
            "lessons",
            "phases",
            "is_enrolled",
            "created_at",
            "updated_at",
        )

    def get_phases(self, obj):
        from .quizgen import generate_phase_plan

        fresh = {p["phase_number"]: p for p in generate_phase_plan(obj.title)}
        phases = obj.phases.all().order_by("phase_number")
        out = []
        for p in phases:
            row = fresh.get(p.phase_number)
            if row:
                out.append(
                    {
                        "id": p.id,
                        "phase_number": p.phase_number,
                        "title": row["title"],
                        "description": row["description"],
                        "content": row["content"],
                        "resources": row["resources"],
                    }
                )
            else:
                out.append(
                    {
                        "id": p.id,
                        "phase_number": p.phase_number,
                        "title": p.title,
                        "description": p.description,
                        "content": p.content,
                        "resources": p.resources,
                    }
                )
        return out

    def get_is_enrolled(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        return Enrollment.objects.filter(user=user, course=obj).exists()


class CourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "title",
            "slug",
            "subtitle",
            "description",
            "learning_outcomes",
            "related_topics",
            "requirements",
            "category",
            "tags",
            "level",
            "pricing",
            "price_cents",
            "duration_minutes",
            "duration_months",
            "thumbnail",
            "thumbnail_url",
            "promo_video",
            "status",
        )

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        validated_data["instructor"] = self.context["request"].user
        course = Course.objects.create(**validated_data)
        course.tags.set(tags)
        return course

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    course_slug = serializers.SlugField(source="course.slug", read_only=True)

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "course",
            "course_slug",
            "course_title",
            "enrolled_at",
            "last_lesson",
            "progress_percent",
            "completed_at",
        )


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ("id", "lesson", "completed", "last_position_seconds", "updated_at")


class LessonBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonBookmark
        fields = ("id", "lesson", "created_at")
        read_only_fields = ("created_at",)


class LessonNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonNote
        fields = ("id", "lesson", "body", "updated_at")


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ("id", "course", "author", "title", "body", "created_at")
        read_only_fields = ("author", "created_at")


class CertificateSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Certificate
        fields = ("id", "course", "course_title", "code", "pdf_file", "issued_at")


class CoursePhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePhase
        fields = ("id", "course", "phase_number", "title", "description", "content", "resources")


class CoursePhaseProgressSerializer(serializers.ModelSerializer):
    phase_number = serializers.IntegerField(source="phase.phase_number", read_only=True)
    phase_title = serializers.CharField(source="phase.title", read_only=True)

    class Meta:
        model = CoursePhaseProgress
        fields = (
            "id",
            "phase",
            "phase_number",
            "phase_title",
            "reading_completed",
            "completed",
            "quiz_score_percent",
            "attempts",
            "updated_at",
        )


class PhaseQuizSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(child=serializers.IntegerField(min_value=0, max_value=3))
