import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    """Simple JSON messages — room name URL mein."""

    async def connect(self):
        self.room = self.scope["url_route"]["kwargs"]["room_name"]
        self.group = f"chat_{self.room}"
        user = self.scope.get("user")
        if isinstance(user, AnonymousUser):
            await self.close()
            return
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        user = self.scope.get("user")
        if isinstance(user, AnonymousUser):
            return
        data = json.loads(text_data or "{}")
        msg = (data.get("message") or "").strip()
        if not msg:
            return
        await sync_to_async(ChatMessage.objects.create)(room=self.room, sender=user, message=msg)
        await self.channel_layer.group_send(
            self.group,
            {"type": "chat.message", "message": msg, "sender": user.email},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"sender": event["sender"], "message": event["message"]}))
