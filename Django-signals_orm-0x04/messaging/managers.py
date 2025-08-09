from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Return only unread messages for a given user.
        Uses .only() to fetch only necessary fields.
        """
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).only('id', 'sender', 'receiver', 'content', 'timestamp')
