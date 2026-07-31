from django import template
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from blog.models import Post, Category, Tag
from django.db.models import Count, Q
import re

register = template.Library()

@register.simple_tag
def get_recent_posts(count=5):
    """Get recent published posts"""
    # ✅ FIXED: Use 'created_at' instead of 'created'
    return Post.objects.filter(status='published').order_by('-created_at')[:count]

@register.simple_tag
def get_popular_posts(count=5):
    """Get most viewed posts"""
    return Post.objects.filter(status='published').order_by('-views')[:count]

@register.simple_tag
def get_featured_posts(count=3):
    """Get featured posts"""
    return Post.objects.filter(status='published', featured=True)[:count]

@register.simple_tag
def get_all_categories():
    """Get all categories with post count"""
    return Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0)

@register.simple_tag
def get_all_tags():
    """Get all tags with post count"""
    return Tag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0)

@register.simple_tag
def get_archive_years():
    """Get years with posts"""
    from django.db.models.functions import ExtractYear
    
    years = Post.objects.filter(status='published') \
        .annotate(year=ExtractYear('created_at')) \
        .values('year') \
        .annotate(count=Count('id')) \
        .order_by('-year')
    
    return years

@register.filter(name='truncate_html')
def truncate_html(value, length=100):
    """Truncate HTML content safely"""
    if not value:
        return ''
    
    # Remove HTML tags
    plain_text = strip_tags(value)
    # Remove extra whitespace
    plain_text = re.sub(r'\s+', ' ', plain_text).strip()
    # Truncate
    words = plain_text.split()
    if len(words) > length:
        return ' '.join(words[:length]) + '...'
    return plain_text

@register.filter(name='reading_time')
def reading_time(value):
    """Calculate reading time in minutes"""
    if not value:
        return 1
    
    # Remove HTML tags
    plain_text = strip_tags(value)
    # Count words
    words = len(plain_text.split())
    # Average reading speed: 200 words per minute
    minutes = max(1, round(words / 200))
    
    return minutes

@register.filter(name='is_liked')
def is_liked(post, user):
    """Check if user has liked the post"""
    if not user.is_authenticated:
        return False
    return post.likes.filter(id=user.id).exists()

@register.filter(name='is_bookmarked')
def is_bookmarked(post, user):
    """Check if user has bookmarked the post"""
    if not user.is_authenticated:
        return False
    return post.bookmarks.filter(id=user.id).exists()

@register.filter(name='has_commented')
def has_commented(post, user):
    """Check if user has commented on the post"""
    if not user.is_authenticated:
        return False
    return post.comments.filter(author=user, active=True).exists()

@register.simple_tag
def get_comment_count(post):
    """Get total active comments for a post"""
    return post.comments.filter(active=True).count()

@register.filter(name='get_gravatar')
def get_gravatar(email, size=80):
    """Generate Gravatar URL"""
    import hashlib
    email_hash = hashlib.md5(email.lower().encode()).hexdigest()
    return f'https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon'

@register.filter(name='format_date')
def format_date(date, format_string="%B %d, %Y"):
    """Format date with custom format"""
    if date:
        return date.strftime(format_string)
    return ''

@register.filter(name='capitalize_first')
def capitalize_first(value):
    """Capitalize first letter of each word"""
    if value:
        return value.title()
    return ''

@register.simple_tag
def get_sidebar_posts():
    """Get posts for sidebar"""
    return {
        'recent': Post.objects.filter(status='published').order_by('-created_at')[:5],
        'popular': Post.objects.filter(status='published').order_by('-views')[:5],
        'featured': Post.objects.filter(status='published', featured=True)[:3]
    }

@register.filter(name='social_share_url')
def social_share_url(platform, url, title):
    """Generate social media share URLs"""
    platforms = {
        'twitter': f'https://twitter.com/intent/tweet?text={title}&url={url}',
        'facebook': f'https://www.facebook.com/sharer/sharer.php?u={url}',
        'linkedin': f'https://www.linkedin.com/shareArticle?mini=true&url={url}&title={title}',
        'whatsapp': f'https://api.whatsapp.com/send?text={title} - {url}',
        'reddit': f'https://www.reddit.com/submit?url={url}&title={title}',
        'email': f'mailto:?subject={title}&body={url}',
    }
    return platforms.get(platform, '#')