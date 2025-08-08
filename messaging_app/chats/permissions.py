from rest_framework import permissions


class IsAuthenticatedAndParticipant(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users who are participants
    in the conversation to view or modify messages.
    """

    def has_permission(self, request, view):
        # Check user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow only participants to access the conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        # For Message objects related to a conversation
        if hasattr(obj, 'conversation'):
            is_participant = request.user in obj.conversation.participants.all()

            # Allow only safe methods unless user is participant
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return is_participant

            # Only allow modification by participant
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return is_participant

        return False
