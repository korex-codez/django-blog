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
        
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                profile.last_seen = timezone.now()
                profile.save()
            except Profile.DoesNotExist:
                pass
        
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