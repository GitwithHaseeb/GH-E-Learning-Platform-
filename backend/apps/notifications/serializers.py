from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "body", "read", "created_at", "email_sent")
        read_only_fields = ("email_sent", "created_at")
