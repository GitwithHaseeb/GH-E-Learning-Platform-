from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.courses.models import Enrollment

from .models import (
    Choice,
    CodingAssignment,
    CodingSubmission,
    PeerReview,
    Quiz,
    QuizAttempt,
)
from .serializers import (
    CodingAssignmentSerializer,
    CodingSubmissionSerializer,
    PeerReviewSerializer,
    QuizAttemptSerializer,
    QuizSerializer,
    QuizStudentSerializer,
    QuizSubmitSerializer,
)


class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()

    def get_queryset(self):
        return Quiz.objects.prefetch_related("questions__choices")

    def get_serializer_class(self):
        if self.action == "take":
            return QuizStudentSerializer
        return QuizSerializer

    @action(detail=True, methods=["get"])
    def take(self, request, pk=None):
        quiz = self.get_object()
        if not Enrollment.objects.filter(user=request.user, course=quiz.course).exists():
            raise PermissionDenied()
        return Response(QuizStudentSerializer(quiz).data)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        quiz = self.get_object()
        if not Enrollment.objects.filter(user=request.user, course=quiz.course).exists():
            raise PermissionDenied()
        ser = QuizSubmitSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        answers = ser.validated_data["answers"]
        total = quiz.questions.count()
        if total == 0:
            raise ValidationError("Quiz mein questions nahi.")
        correct = 0
        for q in quiz.questions.all():
            chosen = answers.get(str(q.id)) or answers.get(q.id)
            if chosen is None:
                continue
            if Choice.objects.filter(pk=chosen, question=q, is_correct=True).exists():
                correct += 1
        score = int(correct * 100 / total)
        passed = score >= quiz.pass_mark_percent
        attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz, score_percent=score, passed=passed)
        return Response(QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)


class QuizAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizAttemptSerializer

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).select_related("quiz")


class CodingAssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CodingAssignmentSerializer
    queryset = CodingAssignment.objects.all()


class CodingSubmissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CodingSubmissionSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return CodingSubmission.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        assignment = serializer.validated_data["assignment"]
        if not Enrollment.objects.filter(user=self.request.user, course=assignment.course).exists():
            raise PermissionDenied()
        code = serializer.validated_data.get("code", "")
        auto = _run_simple_autograde(assignment.test_cases_json, code)
        serializer.save(
            user=self.request.user,
            auto_score_percent=auto,
            status=CodingSubmission.Status.AUTO_GRADED,
        )


def _run_simple_autograde(test_cases, code: str) -> int:
    """Bahut simple demo: har test case string match stdin simulation nahi — sirf count return."""
    if not test_cases:
        return 100 if code.strip() else 0
    ok = 0
    for _ in test_cases:
        ok += 1
    return int(ok * 100 / len(test_cases)) if test_cases else 0


class PeerReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PeerReviewSerializer
    queryset = PeerReview.objects.all()
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return PeerReview.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
