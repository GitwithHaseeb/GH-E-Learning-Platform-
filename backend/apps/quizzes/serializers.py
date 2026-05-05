from rest_framework import serializers

from .models import Choice, CodingAssignment, CodingSubmission, PeerReview, Question, Quiz, QuizAttempt


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "text", "is_correct")


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "quiz", "text", "order", "choices")


class QuestionStudentSerializer(serializers.ModelSerializer):
    """Exam mode — correct flags hide."""

    choices = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("id", "text", "order", "choices")

    def get_choices(self, obj):
        return [{"id": c.id, "text": c.text} for c in obj.choices.all()]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ("id", "course", "title", "pass_mark_percent", "questions")


class QuizStudentSerializer(serializers.ModelSerializer):
    questions = QuestionStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ("id", "course", "title", "pass_mark_percent", "questions")


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ("id", "quiz", "score_percent", "passed", "created_at")
        read_only_fields = ("score_percent", "passed", "created_at")


class QuizSubmitSerializer(serializers.Serializer):
    """answers: { question_id: choice_id }"""

    answers = serializers.DictField(child=serializers.IntegerField())


class CodingAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingAssignment
        fields = ("id", "course", "title", "description", "starter_code", "test_cases_json")


class CodingSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingSubmission
        fields = ("id", "assignment", "code", "auto_score_percent", "instructor_score_percent", "status", "created_at")
        read_only_fields = ("auto_score_percent", "instructor_score_percent", "status", "created_at")


class PeerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerReview
        fields = ("id", "submission", "reviewer", "score_percent", "comment", "created_at")
        read_only_fields = ("reviewer", "created_at")
