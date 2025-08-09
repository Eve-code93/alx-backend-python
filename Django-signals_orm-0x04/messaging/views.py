# messaging/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q

from .models import Message

def _gather_thread(root_message):
    """
    Recursively gather a threaded list starting from root_message.
    Returns nested dicts for easy rendering.
    """
    def recurse(msg):
        return {
            'message': msg,
            'replies': [
                recurse(r)
                for r in msg.replies.all().select_related('sender', 'receiver')
            ]
        }
    return recurse(root_message)

@login_required
@cache_page(60)  # cache this view for 60 seconds
def conversation_view(request, other_username):
    """
    Shows conversation between request.user and another user.
    Uses select_related and prefetch_related to reduce queries.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    other = get_object_or_404(User, username=other_username)

    queryset = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other)) |
        (Q(sender=other) & Q(receiver=request.user))
    ).select_related('sender', 'receiver').prefetch_related('replies')

    messages = queryset.order_by('timestamp')

    return render(request, 'messaging/conversation.html', {
        'messages': messages,
        'other': other,
    })

@login_required
def send_message_view(request):
    """
    POST endpoint to create a message.
    Expects: receiver_username, content, optional parent_id
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST allowed")

    from django.contrib.auth import get_user_model
    User = get_user_model()
    receiver_username = request.POST.get('receiver_username')
    content = request.POST.get('content', '').strip()
    parent_id = request.POST.get('parent_id')

    if not receiver_username or not content:
        return HttpResponseBadRequest("receiver_username and content required")

    try:
        receiver = User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        return HttpResponseBadRequest("receiver not found")

    parent = None
    if parent_id:
        try:
            parent = Message.objects.get(pk=parent_id)
        except Message.DoesNotExist:
            parent = None

    msg = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content,
        parent_message=parent
    )

    return JsonResponse({'status': 'ok', 'message_id': msg.pk})

@login_required
def threaded_view(request, msg_id):
    """
    Return a threaded view for a message and all its replies.
    """
    root = get_object_or_404(
        Message.objects
        .select_related('sender', 'receiver')
        .prefetch_related('replies__sender', 'replies__receiver'),
        pk=msg_id
    )
    thread = _gather_thread(root)
    return render(request, 'messaging/threaded.html', {'thread': thread})

@login_required
def unread_messages_view(request):
    """
    Use the custom manager to fetch only unread messages for user.
    """
    msgs = Message.unread.for_user(request.user).select_related('sender', 'receiver')
    return render(request, 'messaging/unread.html', {'messages': msgs})

@login_required
def delete_user_view(request):
    """
    Allow logged-in user to delete their account.
    POST-only for safety.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Use POST to delete account")

    user = request.user
    from django.contrib.auth import logout
    logout(request)
    user.delete()

    return render(request, 'messaging/account_deleted.html')
