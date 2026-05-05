from django.contrib import admin

from .models import CourseReview, InstructorReply, ReviewHelpfulVote


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ("course", "user", "rating", "created_at")


@admin.register(InstructorReply)
class InstructorReplyAdmin(admin.ModelAdmin):
    list_display = ("review", "created_at")


@admin.register(ReviewHelpfulVote)
class ReviewHelpfulVoteAdmin(admin.ModelAdmin):
    list_display = ("review", "user", "vote")
