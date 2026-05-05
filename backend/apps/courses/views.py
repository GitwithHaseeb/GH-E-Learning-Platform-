"""
Course CRUD, enroll, progress, notes, bookmarks, announcements.
"""
from django.db.models import F, Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAdmin, IsInstructorOwnerOrReadOnly, IsInstructorOrReadOnly

from .filters import CourseFilter
from .models import (
    Announcement,
    Category,
    Certificate,
    Course,
    CoursePhase,
    CoursePhaseProgress,
    CoursePhaseQuiz,
    CourseStatus,
    Enrollment,
    Lesson,
    LessonBookmark,
    LessonNote,
    LessonProgress,
    PricingType,
    Tag,
)
from .serializers import (
    AnnouncementSerializer,
    CategorySerializer,
    CertificateSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    CourseWriteSerializer,
    CoursePhaseSerializer,
    CoursePhaseProgressSerializer,
    EnrollmentSerializer,
    LessonBookmarkSerializer,
    LessonDetailSerializer,
    LessonListSerializer,
    LessonNoteSerializer,
    LessonProgressSerializer,
    LessonWriteSerializer,
    PhaseQuizSubmitSerializer,
    TagSerializer,
)
from .quizgen import build_phase_quiz, generate_phase_plan, merge_phase_meta, needs_quiz_refresh, phase_content


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(parent__isnull=True).prefetch_related("children")
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ("title", "subtitle", "description")
    ordering_fields = ("created_at", "average_rating", "enrollments_count", "price_cents", "duration_minutes")
    ordering = ("-created_at",)
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ("list", "retrieve", "featured"):
            return [AllowAny()]
        if self.action in ("enroll", "phases", "submit_phase_quiz", "mark_reading_complete", "announcements"):
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAuthenticated(), IsInstructorOrReadOnly()]
        return [IsAuthenticated(), IsInstructorOwnerOrReadOnly()]

    def get_queryset(self):
        qs = Course.objects.select_related("instructor", "category").prefetch_related("tags", "lessons", "phases")
        user = self.request.user
        if self.action in ("update", "partial_update", "destroy", "publish_request"):
            if user.is_authenticated and user.is_admin:
                return qs
            if user.is_authenticated:
                return qs.filter(instructor=user)
            return qs.none()
        if self.action in ("list", "featured"):
            if user.is_authenticated and self.request.query_params.get("mine") == "1":
                if user.is_instructor or user.is_admin:
                    return qs.filter(instructor=user)
            return qs.filter(status=CourseStatus.PUBLISHED)
        if self.action == "retrieve":
            if user.is_authenticated:
                return qs.filter(Q(status=CourseStatus.PUBLISHED) | Q(instructor=user))
            return qs.filter(status=CourseStatus.PUBLISHED)
        return qs.filter(status=CourseStatus.PUBLISHED)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return CourseWriteSerializer
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseListSerializer

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def featured(self, request):
        qs = Course.objects.filter(status=CourseStatus.PUBLISHED).order_by("-enrollments_count")[:8]
        return Response(CourseListSerializer(qs, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def enroll(self, request, slug=None):
        course = self.get_object()
        if course.status != CourseStatus.PUBLISHED and not request.user.is_admin:
            raise PermissionDenied("Course abhi publish nahi hai.")
        if course.pricing != PricingType.FREE:
            from apps.payments.models import Order, OrderStatus

            has_order = Order.objects.filter(
                user=request.user,
                course=course,
                status=OrderStatus.PAID,
            ).exists()
            if not has_order:
                raise ValidationError("Pehle course purchase karein.")
        enr, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        if created:
            Course.objects.filter(pk=course.pk).update(enrollments_count=F("enrollments_count") + 1)
            # Ensure 5 phases exist for every course
            plan = generate_phase_plan(course.title)
            for p in plan:
                i = p["phase_number"]
                phase, _ = CoursePhase.objects.get_or_create(
                    course=course,
                    phase_number=i,
                    defaults={
                        "title": p["title"],
                        "description": p["description"],
                        "content": p["content"],
                        "resources": p["resources"],
                    },
                )
                CoursePhaseQuiz.objects.get_or_create(
                    phase=phase,
                    defaults={
                        "questions": build_phase_quiz(course.title, i, p),
                        "pass_mark_percent": 66,
                    },
                )
        return Response(EnrollmentSerializer(enr).data, status=status.HTTP_201_CREATED if created else 200)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def phases(self, request, slug=None):
        course = self.get_object()
        if not Enrollment.objects.filter(user=request.user, course=course).exists():
            raise PermissionDenied("Enroll in this course to access phases.")
        phases = list(CoursePhase.objects.filter(course=course).order_by("phase_number"))
        if not phases:
            plan = generate_phase_plan(course.title)
            for pmeta in plan:
                i = pmeta["phase_number"]
                p = CoursePhase.objects.create(
                    course=course,
                    phase_number=i,
                    title=pmeta["title"],
                    description=pmeta["description"],
                    content=pmeta["content"],
                    resources=pmeta["resources"],
                )
                CoursePhaseQuiz.objects.create(
                    phase=p,
                    questions=build_phase_quiz(course.title, i, pmeta),
                    pass_mark_percent=66,
                )
                phases.append(p)
        progress_qs = CoursePhaseProgress.objects.filter(user=request.user, phase__course=course)
        progress_map = {x.phase_id: x for x in progress_qs}
        fresh_plan = {p["phase_number"]: p for p in generate_phase_plan(course.title)}
        data = []
        for ph in phases:
            pr = progress_map.get(ph.id)
            quiz = CoursePhaseQuiz.objects.filter(phase=ph).first()
            if quiz and needs_quiz_refresh(quiz.questions):
                meta = merge_phase_meta(course.title, ph)
                quiz.questions = build_phase_quiz(course.title, ph.phase_number, meta)
                quiz.pass_mark_percent = 66
                quiz.save(update_fields=["questions", "pass_mark_percent"])
            quiz_questions = []
            if quiz:
                # Client ko answers hide karke questions/options bhejte hain
                for q in (quiz.questions or []):
                    quiz_questions.append(
                        {
                            "question": q.get("question", ""),
                            "options": q.get("options", []),
                        }
                    )
            row = fresh_plan.get(ph.phase_number)
            base = CoursePhaseSerializer(ph).data
            if row:
                base["title"] = row["title"]
                base["description"] = row["description"]
                base["content"] = row["content"]
                base["resources"] = row["resources"]
            data.append(
                {
                    **base,
                    "progress": CoursePhaseProgressSerializer(pr).data if pr else None,
                    "quiz_questions": quiz_questions,
                    "pass_mark_percent": quiz.pass_mark_percent if quiz else 66,
                }
            )
        return Response(data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated], url_path=r"phases/(?P<phase_number>\d+)/reading-complete")
    def mark_reading_complete(self, request, slug=None, phase_number=None):
        course = self.get_object()
        if not Enrollment.objects.filter(user=request.user, course=course).exists():
            raise PermissionDenied("Enrollment required.")
        try:
            phase_no = int(phase_number)
        except (TypeError, ValueError):
            return Response({"detail": "Invalid phase number"}, status=400)
        phase = CoursePhase.objects.filter(course=course, phase_number=phase_no).first()
        if not phase:
            return Response({"detail": "Phase not found"}, status=404)
        if phase_no > 1:
            prev_done = CoursePhaseProgress.objects.filter(
                user=request.user,
                phase__course=course,
                phase__phase_number=phase_no - 1,
                completed=True,
            ).exists()
            if not prev_done:
                return Response({"detail": "Complete previous phase quiz first."}, status=400)
        progress, _ = CoursePhaseProgress.objects.get_or_create(user=request.user, phase=phase)
        progress.reading_completed = True
        progress.save(update_fields=["reading_completed", "updated_at"])
        return Response({"detail": f"Phase {phase_no} reading marked complete."})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated], url_path=r"phases/(?P<phase_number>\d+)/quiz")
    def submit_phase_quiz(self, request, slug=None, phase_number=None):
        course = self.get_object()
        if not Enrollment.objects.filter(user=request.user, course=course).exists():
            raise PermissionDenied("Enrollment required.")
        try:
            phase_no = int(phase_number)
        except (TypeError, ValueError):
            return Response({"detail": "Invalid phase number"}, status=400)
        phase = CoursePhase.objects.filter(course=course, phase_number=phase_no).first()
        if not phase:
            return Response({"detail": "Phase not found"}, status=404)
        # Sequential lock: previous phase must be completed
        if phase_no > 1:
            prev_done = CoursePhaseProgress.objects.filter(
                user=request.user,
                phase__course=course,
                phase__phase_number=phase_no - 1,
                completed=True,
            ).exists()
            if not prev_done:
                return Response({"detail": "Complete previous phase first."}, status=400)
        progress, _ = CoursePhaseProgress.objects.get_or_create(user=request.user, phase=phase)
        if not progress.reading_completed:
            return Response({"detail": "Please complete reading material first."}, status=400)

        ser = PhaseQuizSubmitSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        answers = ser.validated_data["answers"]
        quiz = CoursePhaseQuiz.objects.filter(phase=phase).first()
        meta = merge_phase_meta(course.title, phase)
        if not quiz:
            quiz = CoursePhaseQuiz.objects.create(
                phase=phase,
                questions=build_phase_quiz(course.title, phase_no, meta),
                pass_mark_percent=66,
            )
        questions = quiz.questions or []
        if needs_quiz_refresh(questions):
            questions = build_phase_quiz(course.title, phase_no, meta)
            quiz.questions = questions
            quiz.pass_mark_percent = 66
            quiz.save(update_fields=["questions", "pass_mark_percent"])
        if len(answers) != 30:
            return Response({"detail": "Exactly 30 answers are required."}, status=400)
        correct = 0
        for i, q in enumerate(questions):
            if int(q.get("answer_index", -1)) == int(answers[i]):
                correct += 1
        score = int(round(correct * 100 / 30))
        passed = score >= int(quiz.pass_mark_percent)
        progress.attempts += 1
        progress.quiz_score_percent = score
        progress.completed = passed or progress.completed
        progress.save(update_fields=["attempts", "quiz_score_percent", "completed", "updated_at"])

        # Update enrollment percent from completed phases
        completed_phases = CoursePhaseProgress.objects.filter(
            user=request.user, phase__course=course, completed=True
        ).count()
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        if enrollment:
            enrollment.progress_percent = min(100, completed_phases * 20)
            if enrollment.progress_percent >= 100 and not enrollment.completed_at:
                enrollment.completed_at = timezone.now()
            enrollment.save(update_fields=["progress_percent", "completed_at"])
            if enrollment.progress_percent >= 100:
                cert, created = Certificate.objects.get_or_create(user=request.user, course=course)
                if created or not cert.pdf_file:
                    from .tasks import generate_certificate_pdf

                    generate_certificate_pdf.apply(args=(request.user.id, course.id))
        wrong = 30 - correct
        min_correct = int((30 * int(quiz.pass_mark_percent) + 99) // 100)
        return Response(
            {
                "phase": phase_no,
                "score_percent": score,
                "passed": passed,
                "correct": correct,
                "wrong": wrong,
                "total_questions": 30,
                "pass_mark_percent": int(quiz.pass_mark_percent),
                "min_correct_required": min_correct,
                "required": quiz.pass_mark_percent,
                "course_progress_percent": enrollment.progress_percent if enrollment else 0,
            }
        )

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def announcements(self, request, slug=None):
        course = self.get_object()
        if not Enrollment.objects.filter(user=request.user, course=course).exists() and not (
            request.user.is_admin or request.user == course.instructor
        ):
            raise PermissionDenied()
        data = Announcement.objects.filter(course=course)
        return Response(AnnouncementSerializer(data, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsInstructorOwnerOrReadOnly])
    def publish_request(self, request, slug=None):
        course = self.get_object()
        course.status = CourseStatus.PENDING
        course.save(update_fields=["status"])
        return Response({"detail": "Review ke liye bhej diya.", "status": course.status})


class AdminCourseViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Course.objects.filter(status=CourseStatus.PENDING).select_related("instructor", "category")
    serializer_class = CourseWriteSerializer
    lookup_field = "slug"

    @action(detail=True, methods=["post"])
    def approve(self, request, slug=None):
        course = self.get_object()
        course.status = CourseStatus.PUBLISHED
        course.save(update_fields=["status"])
        return Response({"detail": "Published", "slug": course.slug})

    @action(detail=True, methods=["post"])
    def reject(self, request, slug=None):
        course = self.get_object()
        course.status = CourseStatus.DRAFT
        course.save(update_fields=["status"])
        return Response({"detail": "Rejected to draft"})


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsInstructorOrReadOnly]
    queryset = Lesson.objects.select_related("course", "course__instructor")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return LessonWriteSerializer
        if self.action in ("retrieve",):
            return LessonDetailSerializer
        return LessonListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        course_slug = self.request.query_params.get("course")
        if course_slug:
            qs = qs.filter(course__slug=course_slug)
        return qs

    def perform_create(self, serializer):
        course = serializer.validated_data.get("course")
        if course and course.instructor != self.request.user and not self.request.user.is_admin:
            raise PermissionDenied()
        serializer.save()

    def perform_update(self, serializer):
        lesson = self.get_object()
        if lesson.course.instructor != self.request.user and not self.request.user.is_admin:
            raise PermissionDenied()
        serializer.save()


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related("course", "last_lesson")


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        return LessonProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        lesson = serializer.validated_data["lesson"]
        if not Enrollment.objects.filter(user=self.request.user, course=lesson.course).exists():
            if not lesson.is_preview:
                raise PermissionDenied("Enrollment zaroori hai.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied()
        serializer.save()


class LessonBookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = LessonBookmarkSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return LessonBookmark.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonNoteViewSet(viewsets.ModelViewSet):
    serializer_class = LessonNoteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return LessonNote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated, IsInstructorOrReadOnly]

    def get_queryset(self):
        return Announcement.objects.select_related("course", "author")

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        if course.instructor != self.request.user and not self.request.user.is_admin:
            raise PermissionDenied()
        serializer.save(author=self.request.user)


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user).select_related("course")


class RequestCertificateAPI(APIView):
    """Progress 100% par certificate PDF task trigger (sync apply for local/dev)."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        slug = request.data.get("course_slug")
        if not slug:
            return Response({"detail": "course_slug required"}, status=400)
        course = Course.objects.filter(slug=slug).first()
        if not course:
            return Response({"detail": "Course nahi mila"}, status=404)
        enr = Enrollment.objects.filter(user=request.user, course=course).first()
        if not enr:
            return Response({"detail": "Pehle enroll karein"}, status=400)
        if enr.progress_percent < 100:
            return Response({"detail": "Certificate ke liye 100% completion chahiye"}, status=400)
        from .tasks import generate_certificate_pdf

        generate_certificate_pdf.apply(args=(request.user.id, course.id))
        return Response({"detail": "Certificate generation queued / completed (sync apply)."})


class InstructorAnalyticsAPI(APIView):
    permission_classes = [IsAuthenticated, IsInstructorOrReadOnly]

    def get(self, request):
        if not (request.user.is_instructor or request.user.is_admin):
            raise PermissionDenied()
        from django.db.models import Sum

        from apps.payments.models import Order, OrderStatus

        courses = Course.objects.filter(instructor=request.user)
        total_enroll = Enrollment.objects.filter(course__instructor=request.user).count()
        rev = Order.objects.filter(course__instructor=request.user, status=OrderStatus.PAID).aggregate(
            s=Sum("amount_cents")
        )["s"]
        return Response(
            {
                "courses_count": courses.count(),
                "enrollments_count": total_enroll,
                "revenue_cents": rev or 0,
            }
        )
