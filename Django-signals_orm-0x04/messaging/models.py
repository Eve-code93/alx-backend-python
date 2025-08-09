from django.db import models
from django.conf import settings
from django.utils import timezone

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).only('id', 'sender', 'receiver', 'content', 'timestamp')

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    objects = models.Manager()
    unread = UnreadMessagesManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        snippet = (self.content[:40] + '...') if len(self.content) > 40 else self.content
        return f"#{self.pk} {self.sender} → {self.receiver}: {snippet}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-edited_at']

    def __str__(self):
        return f"History for Message #{self.message_id} at {self.edited_at}"

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Message,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification({self.user}, msg={self.message_id}, read={self.is_read})"
