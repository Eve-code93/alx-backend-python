# messaging/urls.py
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('conversation/<str:other_username>/', views.conversation_view, name='conversation'),
    path('send/', views.send_message_view, name='send_message'),
    path('thread/<int:msg_id>/', views.threaded_view, name='threaded'),
    path('unread/', views.unread_messages_view, name='unread'),
    path('delete-account/', views.delete_user_view, name='delete_user'),
]
