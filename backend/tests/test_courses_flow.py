import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User, UserRole
from apps.courses.models import (
    Category,
    Certificate,
    Course,
    CourseLevel,
    CoursePhaseQuiz,
    CourseStatus,
    Enrollment,
    PricingType,
)
from apps.courses.quizgen import generate_phase_plan


@pytest.mark.django_db
def test_phase_plan_resources_are_topic_specific():
    titles = [
        "Python for Beginners",
        "Web Development Intro",
        "Mobile App Development with Flutter",
        "System Design for Engineers",
        "Cybersecurity Fundamentals",
        "Kubernetes Essentials",
    ]
    must_contain = {
        "Python for Beginners": ["python.org", "freecodecamp.org"],
        "Web Development Intro": ["developer.mozilla.org", "freecodecamp.org"],
        "Mobile App Development with Flutter": ["docs.flutter.dev", "dart.dev"],
        "System Design for Engineers": ["github.com/donnemartin/system-design-primer"],
        "Cybersecurity Fundamentals": ["owasp.org"],
        "Kubernetes Essentials": ["kubernetes.io"],
    }

    for title in titles:
        phases = generate_phase_plan(title)
        assert len(phases) == 5
        for phase in phases:
            reading = phase["resources"]["reading"]
            videos = phase["resources"]["videos"]
            assert reading, f"reading missing for {title} phase {phase['phase_number']}"
            assert videos, f"videos missing for {title} phase {phase['phase_number']}"
            for row in reading:
                assert row["title"]
                assert row["url"].startswith("http")
        links_blob = " ".join(r["url"] for p in phases for r in p["resources"]["reading"])
        for token in must_contain[title]:
            assert token in links_blob, f"{title} does not include expected token {token}"


@pytest.mark.django_db
def test_user_gets_certificate_after_completing_all_5_phases():
    client = APIClient()
    instructor = User.objects.create_user(
        email="inst-course@test.com",
        password="Testpass123!",
        role=UserRole.INSTRUCTOR,
    )
    student = User.objects.create_user(
        email="stu-course@test.com",
        password="Testpass123!",
        role=UserRole.STUDENT,
    )
    category = Category.objects.create(name="Technology", slug="technology")
    course = Course.objects.create(
        title="Python for Beginners",
        slug="python-for-beginners-test",
        subtitle="Test subtitle",
        description="Test description",
        instructor=instructor,
        category=category,
        level=CourseLevel.BEGINNER,
        pricing=PricingType.FREE,
        status=CourseStatus.PUBLISHED,
    )

    client.force_authenticate(user=student)
    enroll = client.post(f"/api/v1/courses/{course.slug}/enroll/")
    assert enroll.status_code in (200, 201)

    # Complete all phases in order with perfect answers.
    for phase_no in range(1, 6):
        marked = client.post(f"/api/v1/courses/{course.slug}/phases/{phase_no}/reading-complete/")
        assert marked.status_code == 200

        quiz = CoursePhaseQuiz.objects.get(phase__course=course, phase__phase_number=phase_no)
        answers = [q["answer_index"] for q in quiz.questions]
        submit = client.post(
            f"/api/v1/courses/{course.slug}/phases/{phase_no}/quiz/",
            {"answers": answers},
            format="json",
        )
        assert submit.status_code == 200
        assert submit.data["passed"] is True

    enrollment = Enrollment.objects.get(user=student, course=course)
    assert enrollment.progress_percent == 100
    assert enrollment.completed_at is not None
    cert = Certificate.objects.get(user=student, course=course)
    assert cert.pdf_file

    cert_list = client.get("/api/v1/student/certificates/")
    assert cert_list.status_code == 200
    items = cert_list.data.get("results", cert_list.data)
    assert any(x.get("course_title") == course.title for x in items)
