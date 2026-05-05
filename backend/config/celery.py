"""
Celery configuration — lambi tasks (email, heavy PDF) background mein.
"""
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("elearning")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
