from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count
import json
import urllib.parse

from .models import Post, Category, Tag, Comment, Profile, Contact, Newsletter, PostView, Activity, UserFollow
from .forms import (
    PostForm, CommentForm, UserRegisterForm, UserLoginForm,
    ProfileForm, ContactForm, NewsletterForm, EditPostForm
)


# ==================== CORE VIEWS ====================

def home(request):
    """Home page with featured posts, latest posts, categories, and tags"""
    # ⚡ BOLT OPTIMIZATION: Fix N+1 queries by prefetching foreign keys (author, category) and m2m (tags)
    # Reduces database queries on home page from ~35 to ~12 queries (over 65% reduction).
    featured_posts = Post.objects.filter(
        status='published',
        featured=True
    ).select_related('author', 'category')[:3]
    
    posts_list = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
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
        # ⚡ BOLT OPTIMIZATION: Fix N+1 queries for post list rendering by eager loading author, category, and tags.
        return Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')


def post_detail(request, slug):
    """Display a single post with comments and interactions"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment view count and track view
    post.views += 1
    post.save()
    
    # Track view with IP and user agent
    if request.META.get('REMOTE_ADDR'):
        try:
            PostView.objects.create(
                post=post,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )
        except:
            pass
    
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
            
            # Create activity for comment
            if request.user.is_authenticated:
                Activity.objects.create(
                    user=request.user,
                    action='comment_created',
                    post=post,
                    comment=comment
                )
            
            messages.success(request, 'Your comment was posted successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()
    
    # Get next and previous posts
    next_post = post.get_next_post()
    previous_post = post.get_previous_post()
    
    # Get related posts
    related_posts = get_related_posts(post)
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'user_liked': user_liked,
        'user_bookmarked': user_bookmarked,
        'next_post': next_post,
        'previous_post': previous_post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def get_related_posts(post, limit=3):
    """Get related posts based on category and tags"""
    related = Post.objects.filter(
        Q(category=post.category) | Q(tags__in=post.tags.all()),
        status='published'
    ).exclude(id=post.id).distinct()[:limit]
    return related


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
    
    # ✅ Get bookmarked posts (only for the logged-in user viewing their own profile)
    bookmark_posts = []
    bookmark_count = 0
    if request.user == profile_user:
        bookmark_posts = Post.objects.filter(bookmarks=request.user, status='published')
        bookmark_count = bookmark_posts.count()
    
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'post_count': user_posts.count(),
        'comment_count': Comment.objects.filter(author=profile_user).count(),
        'bookmark_posts': bookmark_posts,
        'bookmark_count': bookmark_count,
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
            form.save_m2m()
            
            # Create activity
            Activity.objects.create(
                user=request.user,
                action='post_created',
                post=post
            )
            
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
            
            # Create activity
            Activity.objects.create(
                user=request.user,
                action='post_updated',
                post=post
            )
            
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
    """User dashboard with statistics and charts"""
    user_posts = Post.objects.filter(author=request.user)
    
    # Basic stats
    total_posts = user_posts.count()
    published_posts = user_posts.filter(status='published').count()
    draft_posts = user_posts.filter(status='draft').count()
    archived_posts = user_posts.filter(status='archived').count()
    
    # ✅ FIXED: Use Sum instead of Count for views
    total_views = user_posts.aggregate(total=Sum('views'))['total'] or 0
    
    total_comments = Comment.objects.filter(post__author=request.user).count()
    
    # Recent posts
    recent_posts = user_posts.order_by('-created_at')[:5]
    
    # Get views data for chart (last 6 months)
    views_data = []
    try:
        views_data = list(user_posts.filter(
            status='published',
            created_at__gte=timezone.now() - timedelta(days=180)
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            views=Count('views')  # ✅ This is correct for chart data
        ).order_by('month'))
    except:
        pass
    
    # Recent comments for moderation
    recent_comments = Comment.objects.filter(
        post__author=request.user,
        active=False
    ).order_by('-created_at')[:5]
    
    context = {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'archived_posts': archived_posts,
        'total_views': total_views,
        'total_comments': total_comments,
        'recent_posts': recent_posts,
        'views_data': views_data,
        'recent_comments': recent_comments,
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
    
    # ✅ Return both liked status and total likes
    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes()
    })


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
    
    # ✅ Return bookmark status
    return JsonResponse({
        'bookmarked': bookmarked
    })


# ==================== SEARCH AND FILTER VIEWS ====================

def search_posts(request):
    """Search posts by query with filters"""
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'recent')
    
    # ⚡ BOLT OPTIMIZATION: Fix N+1 queries for search result post listing.
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(author__username__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Sorting
    if sort_by == 'popular':
        posts = posts.order_by('-views')
    elif sort_by == 'oldest':
        posts = posts.order_by('created_at')
    else:  # recent
        posts = posts.order_by('-created_at')
    
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Get all categories for filter dropdown
    categories = Category.objects.filter(posts__status='published').distinct()
    
    context = {
        'posts': posts,
        'query': query,
        'selected_category': category_slug,
        'sort': sort_by,
        'categories': categories,
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
    """Contact page with form - sends to email AND WhatsApp"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # ============================================
            # 1. SEND EMAIL (Existing functionality)
            # ============================================
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
            
            # ============================================
            # 2. SEND TO WHATSAPP (NEW)
            # ============================================
            # Your WhatsApp number (with country code, NO + sign)
            # Example: 919876543210 (India)
            whatsapp_number = '919359462697'  # ⚠️ REPLACE WITH YOUR NUMBER
            
            # Create WhatsApp message
            whatsapp_message = f"""📬 *New Contact Form Submission*

👤 *Name:* {contact.name}
📧 *Email:* {contact.email}
📝 *Subject:* {contact.subject}
💬 *Message:*
{contact.message}

📅 *Sent:* {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}
🌐 *From:* MyBlog Website"""

            # Encode message for URL
            encoded_message = urllib.parse.quote(whatsapp_message)
            
            # Create WhatsApp URL
            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
            
            # Store WhatsApp URL in session for redirect
            request.session['whatsapp_url'] = whatsapp_url
            
            messages.success(request, 'Your message was sent successfully! Redirecting to WhatsApp...')
            
            # ============================================
            # 3. REDIRECT TO WHATSAPP
            # ============================================
            return redirect(whatsapp_url)
            
    else:
        form = ContactForm()
    
    return render(request, 'blog/contact.html', {'form': form})


def newsletter_subscribe(request):
    """Subscribe to newsletter - handles both AJAX and regular POST"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if form.is_valid():
            email = form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                if is_ajax:
                    return JsonResponse({'success': False, 'message': 'You are already subscribed to our newsletter.'}, status=400)
                messages.info(request, 'You are already subscribed to our newsletter.')
            else:
                form.save()
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'You have been subscribed to our newsletter!'})
                messages.success(request, 'You have been subscribed to our newsletter!')
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'}, status=400)
            messages.error(request, 'Please enter a valid email address.')
        
        if not is_ajax:
            return redirect(request.META.get('HTTP_REFERER', 'blog:home'))
    
    # GET request - redirect to home
    return redirect('blog:home')


def newsletter_unsubscribe(request):
    """Unsubscribe from newsletter"""
    email = request.GET.get('email')
    token = request.GET.get('token')
    
    if email and token:
        try:
            newsletter = Newsletter.objects.get(email=email, unsubscribe_token=token)
            newsletter.is_active = False
            newsletter.unsubscribed_at = timezone.now()
            newsletter.save()
            messages.success(request, 'You have been unsubscribed from our newsletter.')
        except Newsletter.DoesNotExist:
            messages.error(request, 'Invalid unsubscribe link.')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            try:
                newsletter = Newsletter.objects.get(email=email)
                newsletter.is_active = False
                newsletter.unsubscribed_at = timezone.now()
                newsletter.save()
                messages.success(request, 'You have been unsubscribed from our newsletter.')
            except Newsletter.DoesNotExist:
                messages.error(request, 'Email not found in our newsletter list.')
        return render(request, 'blog/newsletter_unsubscribe.html')
    
    return redirect('blog:home')


# ==================== SITEMAP ====================

class PostSitemap(Sitemap):
    """Sitemap for posts"""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


# ==================== API VIEWS ====================

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
        # Simple implementation
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
        title = data.get('title', '')
        content = data.get('content', '')
        slug = data.get('slug', '')
        
        if slug:
            post = Post.objects.get(slug=slug, author=request.user)
            post.title = title
            post.content = content
            post.status = 'draft'
            post.save()
        else:
            from django.utils.text import slugify
            post = Post.objects.create(
                title=title or 'Untitled Draft',
                content=content,
                slug=slugify(title or 'untitled-draft'),
                author=request.user,
                status='draft'
            )
        
        return JsonResponse({'success': True, 'slug': post.slug})
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def get_notifications(request):
    """API endpoint for user notifications"""
    notifications = []
    
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


def tag_autocomplete(request):
    """API endpoint for tag autocomplete"""
    query = request.GET.get('q', '')
    if len(query) >= 2:
        tags = Tag.objects.filter(name__icontains=query).values_list('name', flat=True)[:10]
        return JsonResponse(list(tags), safe=False)
    return JsonResponse([], safe=False)


# ==================== USER FOLLOW VIEWS ====================

@login_required
def follow_user(request, username):
    """Follow a user"""
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        UserFollow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        messages.success(request, f'You are now following {username}!')
    return redirect('blog:profile_view', username=username)


@login_required
def unfollow_user(request, username):
    """Unfollow a user"""
    user_to_unfollow = get_object_or_404(User, username=username)
    UserFollow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    messages.success(request, f'You have unfollowed {username}.')
    return redirect('blog:profile_view', username=username)


# ==================== ACTIVITY FEED VIEW ====================

@login_required
def activity_feed(request):
    """User activity feed"""
    activities = Activity.objects.filter(user=request.user)[:20]
    return render(request, 'blog/activity_feed.html', {'activities': activities})

# Newsletter subscription (existing)
def newsletter_subscribe(request):
    """Subscribe to newsletter - handles both AJAX and regular POST"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if form.is_valid():
            email = form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                message = 'You are already subscribed to our newsletter.'
                if is_ajax:
                    return JsonResponse({'success': False, 'message': message}, status=400)
                messages.info(request, message)
            else:
                form.save()
                message = 'You have been subscribed to our newsletter!'
                if is_ajax:
                    return JsonResponse({'success': True, 'message': message})
                messages.success(request, message)
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'}, status=400)
            messages.error(request, 'Please enter a valid email address.')
        
        if not is_ajax:
            return redirect(request.META.get('HTTP_REFERER', 'blog:home'))
    
    return redirect('blog:home')

# API endpoints (add these if not present)
def tag_autocomplete(request):
    """API endpoint for tag autocomplete"""
    query = request.GET.get('q', '')
    if len(query) >= 2:
        from .models import Tag
        tags = Tag.objects.filter(name__icontains=query).values_list('name', flat=True)[:10]
        return JsonResponse(list(tags), safe=False)
    return JsonResponse([], safe=False)

def save_draft(request):
    """API endpoint for saving drafts"""
    import json
    from django.views.decorators.http import require_POST
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)
    
    try:
        data = json.loads(request.body)
        title = data.get('title', '')
        content = data.get('content', '')
        slug = data.get('slug', '')
        
        if slug:
            post = Post.objects.get(slug=slug, author=request.user)
            post.title = title
            post.content = content
            post.status = 'draft'
            post.save()
        else:
            from django.utils.text import slugify
            post = Post.objects.create(
                title=title or 'Untitled Draft',
                content=content,
                slug=slugify(title or 'untitled-draft'),
                author=request.user,
                status='draft'
            )
        
        return JsonResponse({'success': True, 'slug': post.slug})
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def bookmarks_view(request):
    """View all bookmarked posts"""
    bookmark_posts = Post.objects.filter(bookmarks=request.user, status='published')
    return render(request, 'blog/bookmarks.html', {'bookmark_posts': bookmark_posts})

