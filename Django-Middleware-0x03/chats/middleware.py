# chats/middleware.py

from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils.timezone import now
from collections import defaultdict
import logging

# Set up logging to a file
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

# Task 1: Logging User Requests
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


# Task 2: Restrict Chat Access by Time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow only between 6PM and 9PM (18 - 21 hours)
        current_hour = datetime.now().hour
        if not (18 <= current_hour < 21):
            return JsonResponse(
                {"error": "Chat access allowed only between 6PM and 9PM"},
                status=403
            )
        return self.get_response(request)


# Task 3: Rate Limiting by IP (5 messages/minute)
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(list)  # {ip: [timestamp, ...]}

    def __call__(self, request):
        if request.method == "POST" and "/messages/" in request.path:
            ip = self.get_client_ip(request)
            now_time = now()
            self.message_log[ip] = [
                timestamp for timestamp in self.message_log[ip]
                if now_time - timestamp < timedelta(minutes=1)
            ]

            if len(self.message_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            self.message_log[ip].append(now_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


# Task 4: Role-Based Permissions
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Apply only to protected admin/moderator routes
        protected_paths = ['/api/conversations/', '/api/messages/']
        if any(request.path.startswith(p) for p in protected_paths):
            user = request.user
            if not user.is_authenticated or user.role not in ['admin', 'moderator']:
                return JsonResponse(
                    {"error": "Permission denied. Only admin or moderator allowed."},
                    status=403
                )
        return self.get_response(request)
