from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.core import serializers
from django.core.paginator import Paginator
from .models import Post, Comment, Category, Tag
from .decorators import ajax_required
import json

@require_GET
def search_autocomplete(request):
    """Search autocomplete API endpoint"""
    query = request.GET.get('q', '')
    if len(query) >= 2:
        posts = Post.objects.filter(
            status='published',
            title__icontains=query
        )[:10]
        results = [{
            'label': post.title,
            'value': post.slug,
            'category': post.category.name if post.category else None
        } for post in posts]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required
@ajax_required
@require_POST
def comment_vote(request):
    """Vote on a comment"""
    try:
        data = json.loads(request.body)
        comment_id = data.get('comment_id')
        vote_type = data.get('vote_type')  # 'up' or 'down'
        
        comment = Comment.objects.get(id=comment_id, active=True)
        
        # Simple voting logic (you can extend this)
        if vote_type == 'up':
            # You might want to track votes in a separate model
            votes = getattr(comment, 'votes', 0) + 1
            comment.votes = votes
            comment.save()
            return JsonResponse({'success': True, 'votes': votes})
        elif vote_type == 'down':
            votes = getattr(comment, 'votes', 0) - 1
            comment.votes = votes
            comment.save()
            return JsonResponse({'success': True, 'votes': votes})
        
        return JsonResponse({'success': False, 'error': 'Invalid vote type'}, status=400)
        
    except Comment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Comment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_GET
def post_stats(request, slug):
    """Get statistics for a post"""
    try:
        post = Post.objects.get(slug=slug, status='published')
        data = {
            'title': post.title,
            'views': post.views,
            'likes': post.total_likes(),
            'comments': post.total_comments(),
            'created_at': post.created_at.isoformat(),
        }
        return JsonResponse(data)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

@require_GET
def recent_posts_api(request):
    """API endpoint for recent posts"""
    limit = int(request.GET.get('limit', 5))
    posts = Post.objects.filter(status='published').order_by('-created_at')[:limit]
    
    data = [{
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'excerpt': post.excerpt,
        'author': post.author.username,
        'created_at': post.created_at.isoformat(),
        'featured_image': post.featured_image.url if post.featured_image else None,
    } for post in posts]
    
    return JsonResponse(data, safe=False)

@require_GET
def popular_posts_api(request):
    """API endpoint for popular posts"""
    limit = int(request.GET.get('limit', 5))
    posts = Post.objects.filter(status='published').order_by('-views')[:limit]
    
    data = [{
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'views': post.views,
        'likes': post.total_likes(),
    } for post in posts]
    
    return JsonResponse(data, safe=False)

@require_GET
def categories_api(request):
    """API endpoint for categories"""
    categories = Category.objects.filter(
        posts__status='published'
    ).distinct()
    
    data = [{
        'id': cat.id,
        'name': cat.name,
        'slug': cat.slug,
        'post_count': cat.posts.filter(status='published').count(),
    } for cat in categories]
    
    return JsonResponse(data, safe=False)

@require_GET
def tags_api(request):
    """API endpoint for tags"""
    tags = Tag.objects.filter(
        posts__status='published'
    ).distinct()
    
    data = [{
        'id': tag.id,
        'name': tag.name,
        'slug': tag.slug,
        'post_count': tag.posts.filter(status='published').count(),
    } for tag in tags]
    
    return JsonResponse(data, safe=False)

@login_required
@ajax_required
@require_POST
def save_post_draft(request):
    """Save post as draft via AJAX"""
    try:
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        slug = data.get('slug')
        
        if slug:
            post = Post.objects.get(slug=slug, author=request.user)
            post.title = title
            post.content = content
            post.status = 'draft'
            post.save()
        else:
            from django.utils.text import slugify
            post = Post.objects.create(
                title=title,
                content=content,
                slug=slugify(title),
                author=request.user,
                status='draft'
            )
        
        return JsonResponse({
            'success': True,
            'slug': post.slug,
            'message': 'Draft saved successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@ajax_required
@require_POST
def get_notifications(request):
    """Get user notifications (simplified)"""
    # This is a simplified version - you'd want a proper notification system
    notifications = []
    
    # Check for new comments on user's posts
    if request.user.is_authenticated:
        recent_comments = Comment.objects.filter(
            post__author=request.user,
            created_at__gte=timezone.now() - timedelta(days=1)
        ).count()
        
        if recent_comments > 0:
            notifications.append({
                'type': 'comment',
                'message': f'You have {recent_comments} new comment(s)',
                'count': recent_comments
            })
    
    return JsonResponse({'notifications': notifications})

# Helper imports
from django.utils import timezone
from datetime import timedelta