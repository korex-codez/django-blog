from django.core.cache import cache
from .models import Category, Tag
from django.db.models import Count, Q

def base_context(request):
    """Context processor to make categories and tags available globally.
    
    PERFORMANCE OPTIMIZATION:
    Cache global categories and tags for 300 seconds (5 minutes) using Django's cache framework.
    This eliminates 2 heavy database aggregation queries on EVERY single HTTP request.
    Expected impact: Saves 2 SQL queries per page load across all pages.
    """
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
