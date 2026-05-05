"""Celery tasks — certificate PDF background mein."""

import io
from datetime import date

from celery import shared_task
from django.core.files.base import ContentFile
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from apps.courses.models import Certificate, Course, Enrollment, Lesson, LessonProgress


@shared_task
def generate_certificate_pdf(user_id: int, course_id: int):
    """Generate certificate PDF in a fixed template with dynamic student/course/date fields."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.filter(pk=user_id).first()
    course = Course.objects.filter(pk=course_id).first()
    if not user or not course:
        return None
    cert, created = Certificate.objects.get_or_create(user=user, course=course)
    if not created and cert.pdf_file:
        return cert.id

    enrollment = Enrollment.objects.filter(user=user, course=course).first()
    start_dt = enrollment.enrolled_at.date() if enrollment and enrollment.enrolled_at else date.today()
    end_dt = enrollment.completed_at.date() if enrollment and enrollment.completed_at else date.today()
    issued_dt = timezone.now().date()
    student_name = f"{user.first_name} {user.last_name}".strip() or user.email

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter

    # Border frame
    c.setStrokeColor(colors.HexColor("#24345E"))
    c.setLineWidth(2)
    c.rect(0.45 * inch, 0.75 * inch, w - 0.9 * inch, h - 1.5 * inch, stroke=1, fill=0)
    c.setStrokeColor(colors.HexColor("#F59E0B"))
    c.setLineWidth(1)
    c.rect(0.62 * inch, 0.92 * inch, w - 1.24 * inch, h - 1.84 * inch, stroke=1, fill=0)

    # Header
    c.setFont("Helvetica-Bold", 19)
    c.drawCentredString(w / 2, h - 1.55 * inch, "GH- E Learn Platform")
    c.setFillColor(colors.HexColor("#F97316"))
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(w / 2, h - 2.35 * inch, "CERTIFICATE OF COMPLETION")
    c.setFillColor(colors.black)

    # Body
    c.setFont("Helvetica", 12)
    c.drawCentredString(w / 2, h - 2.95 * inch, "This certificate is awarded to")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w / 2, h - 3.45 * inch, student_name)

    c.setFont("Helvetica", 12)
    c.drawCentredString(
        w / 2,
        h - 4.10 * inch,
        f"for completing the {course.title} training program",
    )
    c.drawCentredString(
        w / 2,
        h - 4.40 * inch,
        f"from {start_dt.strftime('%d %b %Y')} to {end_dt.strftime('%d %b %Y')}",
    )
    c.drawCentredString(w / 2, h - 4.90 * inch, f"Given on {issued_dt.strftime('%d %b %Y')}")

    # Footer
    c.setFont("Helvetica", 11)
    c.drawCentredString(w / 2, h - 5.55 * inch, f"Verification code: {cert.code}")
    c.line(w / 2 - 70, h - 6.15 * inch, w / 2 + 70, h - 6.15 * inch)
    c.drawCentredString(w / 2, h - 6.35 * inch, "GHANIA & HASEEB")

    c.showPage()
    c.save()
    cert.pdf_file.save(f"{cert.code}.pdf", ContentFile(buf.getvalue()), save=True)
    return cert.id


@shared_task
def recalc_enrollment_progress(enrollment_id: int):
    """Lesson progress se enrollment.progress_percent update."""
    enr = Enrollment.objects.filter(pk=enrollment_id).select_related("course").first()
    if not enr:
        return
    total = Lesson.objects.filter(course=enr.course).count()
    if total == 0:
        return
    done = LessonProgress.objects.filter(user=enr.user, lesson__course=enr.course, completed=True).count()
    enr.progress_percent = min(100, int(done * 100 / total))
    if enr.progress_percent >= 100 and not enr.completed_at:
        enr.completed_at = timezone.now()
        cert, created = Certificate.objects.get_or_create(user=enr.user, course=enr.course)
        enr.save(update_fields=["progress_percent", "completed_at"])
        if created or not cert.pdf_file:
            generate_certificate_pdf.apply(args=(enr.user.id, enr.course.id))
    else:
        enr.save(update_fields=["progress_percent"])
