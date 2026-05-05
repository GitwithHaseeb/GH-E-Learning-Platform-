from django.contrib import admin

from .models import Choice, CodingAssignment, CodingSubmission, PeerReview, Question, Quiz, QuizAttempt


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "pass_mark_percent")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "order")
    inlines = [ChoiceInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score_percent", "passed", "created_at")


@admin.register(CodingAssignment)
class CodingAssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "course")


@admin.register(CodingSubmission)
class CodingSubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "assignment", "auto_score_percent", "status")


@admin.register(PeerReview)
class PeerReviewAdmin(admin.ModelAdmin):
    list_display = ("submission", "reviewer", "score_percent")
