# messaging/signals.py
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as DjangoUserModel
from django.db import transaction

from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    When a message is created, create a Notification for the receiver.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving an existing message, if content changed, store old content
    in MessageHistory and mark the message as edited.
    """
    if not instance.pk:
        # new message — nothing to log
        return

    try:
        original = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if original.content != instance.content:
        # store a history entry
        MessageHistory.objects.create(message=instance, old_content=original.content)
        instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
 
    # messages where user was sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # notifications for the user
    Notification.objects.filter(user=instance).delete()

    # MessageHistory entries referencing messages already deleted will be removed
    # via cascade if set on the FK; if any remain (shouldn't), we can clear them:
    MessageHistory.objects.filter(message__isnull=True).delete()
