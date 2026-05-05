from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LessonProgress
from .tasks import recalc_enrollment_progress


@receiver(post_save, sender=LessonProgress)
def on_lesson_progress(sender, instance, **kwargs):
    from .models import Enrollment

    enr = Enrollment.objects.filter(user=instance.user, course=instance.lesson.course).first()
    if enr:
        recalc_enrollment_progress.apply(args=(enr.id,))
