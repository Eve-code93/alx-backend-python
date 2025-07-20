from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class User(serializers.ModelSerializer):  # ✅ renamed from UserSerializer
    class Meta:
        model = CustomUser
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number'
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = User(read_only=True)  # ✅ nested user
    message_body = serializers.CharField(source='content')
    sent_at = serializers.DateTimeField(source='timestamp', read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body',
            'sent_at'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = User(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='message_set')  # ✅ nested relationship

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages'
        ]
