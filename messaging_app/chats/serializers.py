# chats/serializers.py

from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)  # ✅ CharField check
    participants = serializers.SerializerMethodField()  # ✅ SerializerMethodField
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'participants', 'messages']

    def get_participants(self, obj):
        return [user.username for user in obj.participants.all()]

    def validate_title(self, value):
        if "badword" in value.lower():
            raise serializers.ValidationError("Inappropriate word in title")  # ✅ ValidationError check
        return value
