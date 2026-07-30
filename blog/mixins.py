from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

class OwnerRequiredMixin(UserPassesTestMixin):
    """Mixin to check if user is the owner of the object"""
    owner_field = 'author'
    
    def test_func(self):
        obj = self.get_object()
        owner = getattr(obj, self.owner_field, None)
        return self.request.user == owner or self.request.user.is_staff

class SuperuserRequiredMixin(UserPassesTestMixin):
    """Mixin to check if user is a superuser"""
    def test_func(self):
        return self.request.user.is_superuser

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to check if user is staff"""
    def test_func(self):
        return self.request.user.is_staff

class PostExistsMixin:
    """Mixin to check if post exists"""
    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, slug=slug, status='published')

class PaginationMixin:
    """Mixin for pagination"""
    paginate_by = 10
    page_kwarg = 'page'
    
    def get_paginate_by(self, queryset):
        return self.paginate_by

class SearchMixin:
    """Mixin for search functionality"""
    search_fields = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query and self.search_fields:
            from django.db.models import Q
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__icontains': query})
            queryset = queryset.filter(q_objects).distinct()
        
        return queryset

class CacheMixin:
    """Mixin for caching"""
    cache_timeout = 300
    cache_key_prefix = 'view_cache'
    
    def get_cache_key(self):
        return f'{self.cache_key_prefix}_{self.request.path}'
    
    def get_cached_response(self):
        from django.core.cache import cache
        return cache.get(self.get_cache_key())
    
    def set_cached_response(self, response):
        from django.core.cache import cache
        cache.set(self.get_cache_key(), response, self.cache_timeout)