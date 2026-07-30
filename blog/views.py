from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.sitemaps import Sitemap
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.utils import timezone

from .models import Post, Category, Tag, Comment, Profile, Contact, Newsletter
from .forms import (
    PostForm, CommentForm, UserRegisterForm, UserLoginForm,
    ProfileForm, ContactForm, NewsletterForm, EditPostForm
)
import json


# ==================== CORE VIEWS ====================

def home(request):
    """Home page with featured posts, latest posts, categories, and tags"""
    featured_posts = Post.objects.filter(
        status='published',
        featured=True
    )[:3]
    
    posts_list = Post.objects.filter(status='published')
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0)[:8]
    
    tags = Tag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0)[:15]
    
    context = {
        'featured_posts': featured_posts,
        'posts': posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    """List view for all published posts"""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(status='published')


def post_detail(request, slug):
    """Display a single post with comments and interactions"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Check if user liked or bookmarked the post
    user_liked = False
    user_bookmarked = False
    if request.user.is_authenticated:
        user_liked = post.likes.filter(id=request.user.id).exists()
        user_bookmarked = post.bookmarks.filter(id=request.user.id).exists()
    
    # Get top-level comments
    comments = post.comments.filter(active=True, parent=None)
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent = Comment.objects.get(id=parent_id, active=True)
                    comment.parent = parent
                except Comment.DoesNotExist:
                    pass
            comment.save()
            messages.success(request, 'Your comment was posted successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()
    
    # Get next and previous posts
    next_post = post.get_next_post()
    previous_post = post.get_previous_post()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'user_liked': user_liked,
        'user_bookmarked': user_bookmarked,
        'next_post': next_post,
        'previous_post': previous_post,
    }
    return render(request, 'blog/post_detail.html', context)


# ==================== AUTHENTICATION VIEWS ====================

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('blog:home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('blog:home')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('blog:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back {username}!')
                next_url = request.GET.get('next', 'blog:home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('blog:home')


# ==================== PROFILE VIEWS ====================

@login_required
def profile_view(request, username=None):
    """View user profile"""
    if username:
        profile_user = get_object_or_404(User, username=username)
        if profile_user == request.user:
            return redirect('blog:profile')
    else:
        profile_user = request.user
    
    # Get user's published posts
    user_posts = Post.objects.filter(author=profile_user, status='published')
    paginator = Paginator(user_posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'post_count': user_posts.count(),
        'comment_count': Comment.objects.filter(author=profile_user).count(),
    }
    return render(request, 'blog/profile.html', context)


@login_required
def profile_edit(request):
    """Edit user profile"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('blog:profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    
    return render(request, 'blog/profile_edit.html', {'form': form})


# ==================== POST MANAGEMENT VIEWS ====================

@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many fields (tags)
            messages.success(request, 'Your post was created successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


@login_required
def edit_post(request, slug):
    """Edit an existing post"""
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post was updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = EditPostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, slug):
    """Delete a post"""
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post was deleted successfully!')
        return redirect('blog:profile')
    return render(request, 'blog/delete_post.html', {'post': post})


@login_required
def dashboard(request):
    """User dashboard with statistics"""
    user_posts = Post.objects.filter(author=request.user)
    
    # Statistics
    total_posts = user_posts.count()
    published_posts = user_posts.filter(status='published').count()
    draft_posts = user_posts.filter(status='draft').count()
    total_views = user_posts.aggregate(total=Count('views'))['total'] or 0
    total_comments = Comment.objects.filter(post__author=request.user).count()
    
    # Recent posts
    recent_posts = user_posts.order_by('-created_at')[:5]
    
    context = {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_views': total_views,
        'total_comments': total_comments,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/dashboard.html', context)


# ==================== INTERACTION VIEWS ====================

@login_required
@require_POST
def like_post(request, slug):
    """Like or unlike a post"""
    post = get_object_or_404(Post, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})


@login_required
@require_POST
def bookmark_post(request, slug):
    """Bookmark or unbookmark a post"""
    post = get_object_or_404(Post, slug=slug)
    if request.user in post.bookmarks.all():
        post.bookmarks.remove(request.user)
        bookmarked = False
    else:
        post.bookmarks.add(request.user)
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked})


# ==================== SEARCH AND FILTER VIEWS ====================

def search_posts(request):
    """Search posts by query"""
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(status='published') &
            (Q(title__icontains=query) |
             Q(content__icontains=query) |
             Q(excerpt__icontains=query) |
             Q(author__username__icontains=query) |
             Q(category__name__icontains=query) |
             Q(tags__name__icontains=query))
        ).distinct()
    else:
        posts = Post.objects.none()
    
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
        'query': query,
        'result_count': posts.paginator.count if posts else 0,
    }
    return render(request, 'blog/search_results.html', context)


def category_posts(request, slug):
    """Filter posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """Filter posts by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/tag_posts.html', context)


# ==================== STATIC PAGE VIEWS ====================

def about(request):
    """About page"""
    return render(request, 'blog/about.html')


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification
            subject = f"Contact Form: {contact.subject}"
            message = render_to_string('email/contact_email.html', {
                'name': contact.name,
                'email': contact.email,
                'message': contact.message,
            })
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=True,
                html_message=message,
            )
            
            messages.success(request, 'Your message was sent successfully! We\'ll get back to you soon.')
            return redirect('blog:contact')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


def newsletter_subscribe(request):
    """Subscribe to newsletter"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.info(request, 'You are already subscribed to our newsletter.')
            else:
                form.save()
                messages.success(request, 'You have been subscribed to our newsletter!')
        else:
            messages.error(request, 'Please enter a valid email address.')
        return redirect(request.META.get('HTTP_REFERER', 'blog:home'))


# ==================== SITEMAP ====================

class PostSitemap(Sitemap):
    """Sitemap for posts"""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


# ==================== API VIEWS (OPTIONAL) ====================

def search_autocomplete(request):
    """API endpoint for search autocomplete"""
    query = request.GET.get('q', '')
    if len(query) >= 2:
        posts = Post.objects.filter(
            status='published',
            title__icontains=query
        )[:10]
        results = [{'label': post.title, 'value': post.slug} for post in posts]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


@login_required
@require_POST
def comment_vote(request):
    """API endpoint for voting on comments"""
    try:
        data = json.loads(request.body)
        comment_id = data.get('comment_id')
        # Simple implementation - you can expand this
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def post_stats(request, slug):
    """API endpoint for post statistics"""
    try:
        post = Post.objects.get(slug=slug, status='published')
        data = {
            'title': post.title,
            'views': post.views,
            'likes': post.total_likes(),
            'comments': post.total_comments(),
        }
        return JsonResponse(data)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)


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
@require_POST
def save_post_draft(request):
    """API endpoint for saving drafts"""
    try:
        data = json.loads(request.body)
        # Simple implementation
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def get_notifications(request):
    """API endpoint for user notifications"""
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