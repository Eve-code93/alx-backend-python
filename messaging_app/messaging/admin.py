# messaging/admin.py
from django.contrib import admin
from .models import Message, MessageHistory, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'edited', 'read', 'parent_message')
    list_filter = ('edited', 'read', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'edited_at')
    readonly_fields = ('edited_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read',)
