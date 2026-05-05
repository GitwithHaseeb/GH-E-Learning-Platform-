from rest_framework import permissions, viewsets

from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room = self.request.query_params.get("room")
        qs = ChatMessage.objects.select_related("sender")
        if room:
            return qs.filter(room=room)
        return qs.none()
