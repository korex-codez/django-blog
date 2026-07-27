from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Category
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.db.models import Count, Sum
from django.http import JsonResponse

def home(request):
    # All posts
    posts = Post.objects.all()
    # Search functionality
    query = request.GET.get("q")
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    # Category filter
    category = request.GET.get("category")
    if category:
        posts = posts.filter(
            category__name=category
        )
    # Sorting
    sort = request.GET.get("sort")
    if sort == "popular":
        posts = posts.order_by("-views")
    elif sort == "likes":
        posts = posts.annotate(
            total_likes=Count("likes")
        ).order_by("-total_likes")
    else:
        posts = posts.order_by("-created_at")
    # Pagination (6 posts per page)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    # Featured posts
    featured_posts = Post.objects.filter(
        featured=True
    )[:3]
    # Trending posts
    popular_posts = Post.objects.order_by(
        "-views"
    )[:5]
    # Most liked posts
    most_liked = Post.objects.annotate(
        total_likes=Count("likes")
    ).order_by(
        "-total_likes"
    )[:5]
    # Categories
    categories = Category.objects.all()
    context = {
        "posts": posts,
        "query": query,
        "featured_posts": featured_posts,
        "popular_posts": popular_posts,
        "most_liked": most_liked,
        "categories": categories,
    }
    return render(
        request,
        "blog/home.html",
        context
    )


def post_detail(request, id):

    post = get_object_or_404(
        Post,
        id=id
    )


    related_posts = Post.objects.filter(
        category=post.category
    ).exclude(
        id=post.id
    )[:3]


    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "related_posts": related_posts
        }
    )


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(
            username=username,
            password=password
        )
        login(request, user)
        return redirect('home')
    return render(request, 'blog/register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            username=username,
            password=password
        )
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'blog/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    # Only the owner can edit
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    # Only the owner can delete
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == "POST":
        post.delete()
        return redirect('home')
    return render(request, 'blog/delete_post.html', {'post': post})

@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', id=id)

@login_required
def bookmark_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.user in post.bookmarks.all():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)

    return redirect("post_detail", id=id)

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(
        author=request.user
    )
    total_posts = user_posts.count()
    total_likes = user_posts.aggregate(
        total=Count("likes")
    )["total"] or 0
    total_views = user_posts.aggregate(
        total=Sum("views")
    )["total"] or 0
    recent_posts = user_posts.order_by(
        "-created_at"
    )[:5]
    context = {
        "total_posts": total_posts,
        "total_likes": total_likes,
        "total_views": total_views,
        "recent_posts": recent_posts
    }
    return render(
        request,
        "blog/dashboard.html",
        context
    )

@login_required
def profile(request):

    profile = request.user.profile


    posts = Post.objects.filter(
        author=request.user
    )


    return render(
        request,
        "blog/profile.html",
        {
            "profile":profile,
            "posts":posts
        }
    )

def about(request):
    return render(request, "blog/about.html")

def contact(request):
    return render(request, "blog/contact.html")

def custom_404(request, exception):
    return render(request, "blog/404.html", status=404)

def custom_500(request):
    return render(request, "blog/500.html", status=500)

def like_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            "liked": liked,
            "count": post.likes.count()
        })

    return JsonResponse({
        "error":"Login required"
    })

@login_required
def profile_edit(request):

    profile = request.user.profile


    if request.method == "POST":

        profile.bio = request.POST.get("bio")

        if request.FILES.get("image"):

            profile.image = request.FILES["image"]


        profile.save()


        return redirect("profile")



    return render(
        request,
        "blog/profile_edit.html",
        {
            "profile":profile
        }
    )