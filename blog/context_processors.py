from .models import Category, Tag
from django.db.models import Count, Q

def base_context(request):
    """Context processor to make categories and tags available globally"""
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0)[:8]
    
    tags = Tag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0)[:15]
    
    return {
        'categories': categories,
        'tags': tags,
    }