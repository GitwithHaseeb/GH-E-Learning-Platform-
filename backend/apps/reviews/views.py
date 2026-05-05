from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.courses.models import Enrollment

from .models import CourseReview, InstructorReply, ReviewHelpfulVote
from .serializers import CourseReviewSerializer, InstructorReplySerializer, ReviewVoteSerializer


class CourseReviewViewSet(viewsets.ModelViewSet):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_slug = self.request.query_params.get("course")
        qs = CourseReview.objects.select_related("user", "course").prefetch_related("instructor_reply")
        if course_slug:
            qs = qs.filter(course__slug=course_slug)
        return qs

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        if not Enrollment.objects.filter(user=self.request.user, course=course).exists():
            raise PermissionDenied("Sirf enrolled students review likh sakte hain.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied()
        serializer.save()


class InstructorReplyViewSet(viewsets.ModelViewSet):
    queryset = InstructorReply.objects.all()
    serializer_class = InstructorReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return InstructorReply.objects.select_related("review", "review__course")

    def perform_create(self, serializer):
        review = serializer.validated_data["review"]
        if review.course.instructor != self.request.user and not self.request.user.is_admin:
            raise PermissionDenied()
        serializer.save()


class ReviewVoteViewSet(viewsets.ModelViewSet):
    queryset = ReviewHelpfulVote.objects.all()
    serializer_class = ReviewVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return ReviewHelpfulVote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
