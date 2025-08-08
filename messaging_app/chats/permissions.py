from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj could be a Message or Conversation
        conversation = getattr(obj, 'conversation', obj)
        return request.user in conversation.participants.all()
