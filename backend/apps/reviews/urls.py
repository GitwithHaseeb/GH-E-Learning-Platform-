from rest_framework.routers import DefaultRouter

from .views import CourseReviewViewSet, InstructorReplyViewSet, ReviewVoteViewSet

router = DefaultRouter()
router.register("reviews", CourseReviewViewSet)
router.register("review-replies", InstructorReplyViewSet)
router.register("review-votes", ReviewVoteViewSet, basename="review-vote")

urlpatterns = router.urls
