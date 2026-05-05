from django.db.models import Avg, Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import CourseReview


@receiver(post_save, sender=CourseReview)
@receiver(post_delete, sender=CourseReview)
def update_course_rating(sender, instance, **kwargs):
    course = instance.course
    agg = CourseReview.objects.filter(course=course).aggregate(avg=Avg("rating"), n=Count("id"))
    course.average_rating = round(agg["avg"] or 0, 2)
    course.ratings_count = agg["n"] or 0
    course.save(update_fields=["average_rating", "ratings_count"])
