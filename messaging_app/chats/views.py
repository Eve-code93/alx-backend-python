# chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant
from .pagination import MessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_pk']
        conversation = Conversation.objects.get(id=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant in this conversation.", code=status.HTTP_403_FORBIDDEN)

        return Message.objects.filter(conversation=conversation).order_by('-timestamp')

    def perform_create(self, serializer):
        conversation = Conversation.objects.get(id=self.kwargs['conversation_pk'])
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You cannot send a message in this conversation.", code=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.sender:
            raise PermissionDenied(detail="You can only update your own messages.", code=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.sender:
            raise PermissionDenied(detail="You can only delete your own messages.", code=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
