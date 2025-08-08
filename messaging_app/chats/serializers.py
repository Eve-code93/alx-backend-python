from rest_framework import serializers
from .models import Conversation, Message
from .models import CustomUser


class User(serializers.ModelSerializer):
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
    sender = User(read_only=True)
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

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        if "spam" in value.lower():
            raise serializers.ValidationError("Message contains prohibited word: 'spam'.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = User(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages'
        ]

    def get_messages(self, obj):
        messages = obj.message_set.all().order_by('timestamp')
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        participants = self.instance.participants.all() if self.instance else []
        if len(participants) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return data
