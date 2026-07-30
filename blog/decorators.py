from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from functools import wraps

def staff_required(function=None, redirect_field_name='next', login_url='login'):
    """Decorator for staff user access"""
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def superuser_required(function=None, redirect_field_name='next', login_url='login'):
    """Decorator for superuser access"""
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def owner_required(model_field='user'):
    """Decorator to check if user is the owner of the object"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get the object
            obj = view_func.__self__.get_object() if hasattr(view_func, '__self__') else None
            
            if obj and hasattr(obj, model_field):
                owner = getattr(obj, model_field)
                if request.user != owner and not request.user.is_staff:
                    return HttpResponseForbidden("You don't have permission to access this resource.")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def ajax_required(view_func):
    """Decorator to ensure request is AJAX"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponseForbidden("AJAX request required")
        return view_func(request, *args, **kwargs)
    return wrapper

def post_exists(model):
    """Decorator to check if post exists"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            slug = kwargs.get('slug')
            try:
                post = model.objects.get(slug=slug, status='published')
                request.post = post
            except model.DoesNotExist:
                from django.shortcuts import get_object_or_404
                get_object_or_404(model, slug=slug)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def rate_limit(max_attempts=5, timeout_minutes=15):
    """Decorator for rate limiting"""
    from django.core.cache import cache
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Get client IP
                ip = request.META.get('REMOTE_ADDR')
                cache_key = f'rate_limit_{ip}_{view_func.__name__}'
                
                # Get current attempts
                attempts = cache.get(cache_key, 0)
                
                if attempts >= max_attempts:
                    return HttpResponseForbidden("Too many requests. Please try again later.")
                
                # Increment attempts
                cache.set(cache_key, attempts + 1, timeout_minutes * 60)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator