from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CourseReview(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("course", "user")
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["course", "-created_at"])]


class ReviewHelpfulVote(models.Model):
    HELPFUL = "helpful"
    NOT_HELPFUL = "not_helpful"
    VOTE_CHOICES = ((HELPFUL, "Helpful"), (NOT_HELPFUL, "Not helpful"))

    review = models.ForeignKey(CourseReview, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.CharField(max_length=12, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("review", "user")


class InstructorReply(models.Model):
    review = models.OneToOneField(CourseReview, on_delete=models.CASCADE, related_name="instructor_reply")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
