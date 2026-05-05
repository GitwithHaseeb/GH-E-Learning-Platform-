from rest_framework import serializers

from .models import CourseReview, InstructorReply, ReviewHelpfulVote


class InstructorReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorReply
        fields = ("id", "body", "created_at")


class CourseReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    instructor_reply = InstructorReplySerializer(read_only=True)

    class Meta:
        model = CourseReview
        fields = (
            "id",
            "course",
            "user",
            "user_email",
            "rating",
            "title",
            "body",
            "created_at",
            "updated_at",
            "instructor_reply",
        )
        read_only_fields = ("user", "created_at", "updated_at")


class ReviewVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewHelpfulVote
        fields = ("id", "review", "vote")
        read_only_fields = ("user",)
