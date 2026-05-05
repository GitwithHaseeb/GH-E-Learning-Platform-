from django.conf import settings
from django.db import models


class ChatMessage(models.Model):
    room = models.CharField(max_length=120, db_index=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_messages")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        indexes = [models.Index(fields=["room", "created_at"])]
