from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        with open('request.log', 'a') as log_file:
            log_file.write(log_entry)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 18 (6PM) and 21 (9PM)
        if not (18 <= current_hour < 21):
            return Response({'Error:'}, status=status.HTTP_403_FORBIDDEN)
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    message_counts = []

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # for only post request
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = datetime.now()
            window_start = now - timedelta(minutes=1)

            # clean old entries
            if ip in self.message_counts:
                self.message_counts[ip] = [
                    t for t in self.message_counts[ip] if t > window_start
                ]
            else:
                self.message_counts[ip] = []

            # check limit
            if len(self.message_counts[ip]) >= 5:
                return Response({'Error: request too many times'},
                                status=status.HTTP_403_FORBIDDEN)

            # Record the message
            self.message_counts[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        # Check if user is authenticated and has a role attribute
        if not user or not user.is_authenticated:
            return Response({'Error: Not authorised'},
                            status=status.HTTP_403_FORBIDDEN)
        # allow Admin or Moderator
        if getattr(user, 'role', None) not in ['admin', 'moderator']:
            return Response({'Error'}, status=status.HTTP_403_FORBIDDEN)
        response = self.get_response(request)
        return response