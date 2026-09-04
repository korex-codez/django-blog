from django.core.cache import cache
from django.db.models import Count, Q
from .models import Category, Tag

def base_context(request):
    """Context processor to make categories and tags available globally with caching"""
    categories = cache.get('base_categories')
    if categories is None:
        categories = list(Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0)[:8])
        cache.set('base_categories', categories, 300)
    
    tags = cache.get('base_tags')
    if tags is None:
        tags = list(Tag.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0)[:15])
        cache.set('base_tags', tags, 300)
    
    return {
        'categories': categories,
        'tags': tags,
    }