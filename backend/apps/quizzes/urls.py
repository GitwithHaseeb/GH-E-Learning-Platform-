from rest_framework.routers import DefaultRouter

from .views import (
    CodingAssignmentViewSet,
    CodingSubmissionViewSet,
    PeerReviewViewSet,
    QuizAttemptViewSet,
    QuizViewSet,
)

router = DefaultRouter()
router.register("quizzes", QuizViewSet)
router.register("quiz-attempts", QuizAttemptViewSet, basename="quiz-attempt")
router.register("coding-assignments", CodingAssignmentViewSet)
router.register("coding-submissions", CodingSubmissionViewSet, basename="coding-submission")
router.register("peer-reviews", PeerReviewViewSet, basename="peer-review")

urlpatterns = router.urls
