from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from .models import Conversation, Message
from users.models import CustomUser  # assuming your custom user is here


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
    message_body = serializers.CharField(source='content')  # ✅ CharField
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
        if len(value.strip()) == 0:
            raise ValidationError("Message body cannot be empty.")
        if "spam" in value.lower():
            raise ValidationError("Message contains prohibited word: 'spam'.")
        return value


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

    def validate(self, data):
        if 'participants' in data and len(data['participants']) < 2:
            raise ValidationError("A conversation must have at least 2 participants.")
        return data
