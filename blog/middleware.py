from django.utils import timezone
from django.core.cache import cache
from django.conf import settings  # ✅ ADD THIS IMPORT
from .models import Profile
import re


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Performance optimization (Bolt ⚡):
        # Previously, every HTTP request made by an authenticated user triggered Profile.objects.get()
        # followed by profile.save() (2 SQL queries: SELECT + UPDATE on every single page view).
        # We throttle updates using cache (updating at most once every 300 seconds per user) and use direct
        # QuerySet.filter(...).update(...) to bypass model save overhead and eliminate the SELECT query.
        # Expected impact: Eliminates 2 database queries per request for active user sessions within the 5-minute window.
        if request.user.is_authenticated:
            cache_key = f'user_last_seen_{request.user.id}'
            if not cache.get(cache_key):
                Profile.objects.filter(user=request.user).update(last_seen=timezone.now())
                cache.set(cache_key, True, 300)
        
        return response


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = [
            r'^/admin/',
            r'^/static/',
            r'^/media/',
            r'^/favicon.ico',
        ]

    def __call__(self, request):
        # Check if path should be excluded
        path = request.path
        for pattern in self.excluded_paths:
            if re.match(pattern, path):
                return self.get_response(request)
        
        # Track user activity in cache
        if request.user.is_authenticated:
            cache_key = f'user_activity_{request.user.id}'
            cache.set(cache_key, timezone.now(), 300)
        
        response = self.get_response(request)
        return response


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy (CSP)
        csp = "default-src 'self'; "
        csp += "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://code.jquery.com; "
        csp += "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        csp += "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
        csp += "img-src 'self' data: https://*.gravatar.com; "
        csp += "connect-src 'self'; "
        
        # Only add CSP in production
        if not settings.DEBUG:  # ✅ Now 'settings' is defined
            response['Content-Security-Policy'] = csp
        
        return response