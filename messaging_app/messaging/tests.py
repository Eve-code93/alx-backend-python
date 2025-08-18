# messaging/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

class MessagingSignalsTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass')
        self.bob = User.objects.create_user(username='bob', password='pass')

    def test_message_creation_creates_notification(self):
        msg = Message.objects.create(sender=self.alice, receiver=self.bob, content='hi bob')
        self.assertTrue(Notification.objects.filter(user=self.bob, message=msg).exists())

    def test_message_edit_logs_history(self):
        msg = Message.objects.create(sender=self.alice, receiver=self.bob, content='first')
        msg.content = 'edited'
        msg.save()
        self.assertTrue(MessageHistory.objects.filter(message=msg, old_content='first').exists())
        msg.refresh_from_db()
        self.assertTrue(msg.edited)
