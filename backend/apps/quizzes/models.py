import uuid

from django.conf import settings
from django.db import models


class Quiz(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=200)
    pass_mark_percent = models.PositiveSmallIntegerField(default=60)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score_percent = models.PositiveSmallIntegerField(default=0)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CodingAssignment(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="coding_assignments")
    title = models.CharField(max_length=200)
    description = models.TextField()
    starter_code = models.TextField(blank=True)
    test_cases_json = models.JSONField(default=list, help_text="Simple list of {input, expected} for auto-check")

    def __str__(self):
        return self.title


class CodingSubmission(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        AUTO_GRADED = "auto_graded", "Auto graded"
        PEER_REVIEW = "peer_review", "Peer review"
        FINAL = "final", "Final"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="coding_submissions")
    assignment = models.ForeignKey(CodingAssignment, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField()
    auto_score_percent = models.PositiveSmallIntegerField(default=0)
    instructor_score_percent = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)


class PeerReview(models.Model):
    submission = models.ForeignKey(CodingSubmission, on_delete=models.CASCADE, related_name="peer_reviews")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score_percent = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("submission", "reviewer")
