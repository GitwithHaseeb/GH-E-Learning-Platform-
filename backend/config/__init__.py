# Celery app ko Django load par import karein taake shared_task kaam kare
from .celery import app as celery_app

__all__ = ("celery_app",)
