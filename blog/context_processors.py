from .models import Category, Tag
from django.db.models import Count, Q
from django.core.cache import cache

def base_context(request):
    """Context processor to make categories and tags available globally with caching"""
    # Performance Optimization: Cache categories and tags to avoid running heavy aggregate queries on every request
    categories = cache.get('global_categories')
    if categories is None:
        categories = list(Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0)[:8])
        cache.set('global_categories', categories, 300)
    
    tags = cache.get('global_tags')
    if tags is None:
        tags = list(Tag.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0)[:15])
        cache.set('global_tags', tags, 300)
    
    return {
        'categories': categories,
        'tags': tags,
    }