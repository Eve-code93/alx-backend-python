# messaging/apps.py
from django.apps import AppConfig
import django.db.models.signals
import messaging.signals  # Ensure signals are imported to register them
class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        # Import signals to ensure they are registered when the app is ready
        import messaging.signals  # noqa: F401
