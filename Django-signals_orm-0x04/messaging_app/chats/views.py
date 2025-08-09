# chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsAuthenticatedAndParticipant
from .pagination import MessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndParticipant]

    def get_queryset(self):
        """
        Return only conversations the authenticated user is a participant in.
        """
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndParticipant]
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        Return messages from a conversation only if the user is a participant.
        """
        conversation_id = self.kwargs.get('conversation_pk')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(
                detail="You are not a participant in this conversation.",
                code=status.HTTP_403_FORBIDDEN
            )

        return Message.objects.filter(conversation=conversation).order_by('-sent_at')

    def perform_create(self, serializer):
        """
        Save a message only if the sender is a participant in the conversation.
        """
        conversation_id = self.kwargs.get('conversation_pk')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(
                detail="You cannot send a message in this conversation.",
                code=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user, conversation=conversation)

    def update(self, request, *args, **kwargs):
        """
        Allow message update only by the original sender.
        """
        instance = self.get_object()
        if request.user != instance.sender:
            raise PermissionDenied(
                detail="You can only update your own messages.",
                code=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Allow message deletion only by the original sender.
        """
        instance = self.get_object()
        if request.user != instance.sender:
            raise PermissionDenied(
                detail="You can only delete your own messages.",
                code=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
