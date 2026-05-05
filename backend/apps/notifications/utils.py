"""Helper — notification + optional email (Celery se call karein)."""

from django.core.mail import send_mail
from django.conf import settings

from .models import Notification


def notify_user(user, title: str, body: str = "", send_email: bool = False):
    n = Notification.objects.create(user=user, title=title, body=body)
    if send_email and user.email:
        send_mail(
            title,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        n.email_sent = True
        n.save(update_fields=["email_sent"])
    return n
