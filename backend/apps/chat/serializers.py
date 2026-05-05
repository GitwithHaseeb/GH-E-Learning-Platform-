from rest_framework import serializers

from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source="sender.email", read_only=True)

    class Meta:
        model = ChatMessage
        fields = ("id", "room", "sender", "sender_email", "message", "created_at")
        read_only_fields = ("sender", "created_at")
