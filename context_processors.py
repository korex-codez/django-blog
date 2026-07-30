from .models import Category, Tag
from django.db.models import Count, Q

def base_context(request):
    categories = Category.objects.filter(
        posts__status='published'
    ).distinct()[:8]
    
    tags = Tag.objects.filter(
        posts__status='published'
    ).distinct()[:15]
    
    return {
        'categories': categories,
        'tags': tags,
    }