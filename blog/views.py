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

def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    posts = Post.objects.all().order_by('-created_at')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    if category:
        posts = posts.filter(category__id=category)
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'posts': posts,
        'categories': Category.objects.all(),
        'recent_posts': Post.objects.order_by('-created_at')[:5],
        'popular_posts': Post.objects.order_by('-created_at')[:5],   # We'll improve this later
        'query': query,
        'selected_category': category,
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    post.views += 1
    post.save()
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect('post_detail', id=id)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
    })

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
    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    context = {
        'posts': posts,
        'total_posts': posts.count(),
    }

    return render(request, 'blog/dashboard.html', context)

@login_required
def profile(request):

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile_form.save()

            messages.success(request, "Profile Updated Successfully")

            return redirect("profile")

    else:

        user_form = UserUpdateForm(instance=request.user)

        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "blog/profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })

def about(request):
    return render(request, "blog/about.html")

def contact(request):
    return render(request, "blog/contact.html")

def custom_404(request, exception):
    return render(request, "blog/404.html", status=404)

def custom_500(request):
    return render(request, "blog/500.html", status=500)