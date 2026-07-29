from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib.auth.decorators import login_required

from django.http import (
    HttpResponseForbidden,
    JsonResponse,
)

from django.db.models import (
    Q,
    Count,
    Sum,
)

from django.core.paginator import Paginator

from .models import (
    Post,
    Category,
    Comment,
    Profile,
    Newsletter,
    Contact,
)

from .forms import (
    PostForm,
    CommentForm,
    UserUpdateForm,
    ProfileUpdateForm,
    NewsletterForm,
    ContactForm,
)


# ==========================================================
# HOME PAGE
# ==========================================================

def home(request):

    posts = Post.objects.all()

    query = request.GET.get("q")

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    category = request.GET.get("category")

    if category:
        posts = posts.filter(
            category__name=category
        )

    sort = request.GET.get("sort")

    if sort == "popular":
        posts = posts.order_by("-views")

    elif sort == "likes":
        posts = posts.annotate(
            total_likes=Count("likes")
        ).order_by("-total_likes")

    else:
        posts = posts.order_by("-created_at")

    paginator = Paginator(posts, 6)

    page = request.GET.get("page")

    posts = paginator.get_page(page)

    featured_posts = Post.objects.filter(
        featured=True
    )[:3]

    popular_posts = Post.objects.order_by(
        "-views"
    )[:5]

    most_liked = Post.objects.annotate(
        total_likes=Count("likes")
    ).order_by(
        "-total_likes"
    )[:5]

    categories = Category.objects.all()

    newsletter_form = NewsletterForm()

    context = {

        "posts": posts,

        "query": query,

        "featured_posts": featured_posts,

        "popular_posts": popular_posts,

        "most_liked": most_liked,

        "categories": categories,

        "newsletter_form": newsletter_form,

    }

    return render(
        request,
        "blog/home.html",
        context,
    )


# ==========================================================
# POST DETAIL
# ==========================================================

def post_detail(request, id):

    post = get_object_or_404(
        Post,
        id=id
    )

    post.views += 1

    post.save()

    comments = Comment.objects.filter(
        post=post
    ).order_by("-created_at")

    related_posts = Post.objects.filter(
        category=post.category
    ).exclude(
        id=post.id
    )[:3]

    if request.method == "POST":

        if request.user.is_authenticated:

            form = CommentForm(request.POST)

            if form.is_valid():

                comment = form.save(
                    commit=False
                )

                comment.post = post

                comment.user = request.user

                comment.save()

                return redirect(
                    "post_detail",
                    id=post.id
                )

        else:

            messages.error(
                request,
                "Please login first."
            )

            return redirect("login")

    else:

        form = CommentForm()

    return render(

        request,

        "blog/post_detail.html",

        {

            "post": post,

            "comments": comments,

            "form": form,

            "related_posts": related_posts,

        }

    )


# ==========================================================
# REGISTER
# ==========================================================

def register(request):

    if request.method == "POST":

        username = request.POST["username"]

        password = request.POST["password"]

        email = request.POST.get("email")

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password,

        )

        login(request, user)

        return redirect("home")

    return render(
        request,
        "blog/register.html"
    )


# ==========================================================
# LOGIN
# ==========================================================

def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]

        password = request.POST["password"]

        user = authenticate(

            username=username,

            password=password,

        )

        if user:

            login(request, user)

            return redirect("home")

        messages.error(

            request,

            "Invalid username or password."

        )

    return render(
        request,
        "blog/login.html"
    )


# ==========================================================
# LOGOUT
# ==========================================================

def user_logout(request):

    logout(request)

    return redirect("home")


# ==========================================================
# CREATE POST
# ==========================================================

@login_required
def create_post(request):

    if request.method == "POST":

        form = PostForm(

            request.POST,

            request.FILES,

        )

        if form.is_valid():

            post = form.save(
                commit=False
            )

            post.author = request.user

            post.save()

            form.save_m2m()

            messages.success(
                request,
                "Post published successfully."
            )

            return redirect(
                "post_detail",
                id=post.id
            )

    else:

        form = PostForm()

    return render(

        request,

        "blog/create_post.html",

        {

            "form": form

        }

    )

# ==========================================================
# EDIT POST
# ==========================================================

@login_required
def edit_post(request, id):

    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return HttpResponseForbidden("Permission Denied")

    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("post_detail", id=post.id)

    else:

        form = PostForm(instance=post)

    return render(
        request,
        "blog/edit_post.html",
        {
            "form": form
        }
    )


# ==========================================================
# DELETE POST
# ==========================================================

@login_required
def delete_post(request, id):

    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return HttpResponseForbidden("Permission Denied")

    if request.method == "POST":

        post.delete()

        messages.success(
            request,
            "Post deleted successfully."
        )

        return redirect("home")

    return render(
        request,
        "blog/delete_post.html",
        {
            "post": post
        }
    )


# ==========================================================
# LIKE POST (AJAX)
# ==========================================================

@login_required
def like_post(request, id):

    post = get_object_or_404(Post, id=id)

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


# ==========================================================
# BOOKMARK POST
# ==========================================================

@login_required
def bookmark_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.user in post.bookmarks.all():

        post.bookmarks.remove(request.user)

        bookmarked = False

    else:

        post.bookmarks.add(request.user)

        bookmarked = True

    return JsonResponse({

        "bookmarked": bookmarked

    })


# ==========================================================
# DASHBOARD
# ==========================================================

@login_required
def dashboard(request):

    posts = Post.objects.filter(
        author=request.user
    )

    context = {

        "total_posts": posts.count(),

        "total_views": posts.aggregate(
            Sum("views")
        )["views__sum"] or 0,

        "total_likes": posts.aggregate(
            Count("likes")
        )["likes__count"] or 0,

        "recent_posts": posts.order_by(
            "-created_at"
        )[:5],

    }

    return render(
        request,
        "blog/dashboard.html",
        context
    )


# ==========================================================
# PROFILE
# ==========================================================

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
            "profile": profile,
            "posts": posts,
        }
    )


# ==========================================================
# EDIT PROFILE
# ==========================================================

@login_required
def profile_edit(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile_form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=profile
        )

    return render(
        request,
        "blog/profile_edit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )

# ==========================================================
# AUTHOR PROFILE
# ==========================================================

def author_profile(request, username):

    author = get_object_or_404(
        User,
        username=username
    )

    posts = Post.objects.filter(
        author=author
    ).order_by("-created_at")

    return render(
        request,
        "blog/author_profile.html",
        {
            "author": author,
            "posts": posts,
        }
    )


# ==========================================================
# NEWSLETTER
# ==========================================================

def newsletter_subscribe(request):

    if request.method == "POST":

        form = NewsletterForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            if not Newsletter.objects.filter(email=email).exists():

                form.save()

                messages.success(
                    request,
                    "Subscribed successfully!"
                )

            else:

                messages.info(
                    request,
                    "You are already subscribed."
                )

    return redirect("home")


# ==========================================================
# ABOUT
# ==========================================================

def about(request):

    return render(
        request,
        "blog/about.html"
    )


# ==========================================================
# CONTACT
# ==========================================================

def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Message sent successfully."
            )

            return redirect("contact")

    else:

        form = ContactForm()

    return render(
        request,
        "blog/contact.html",
        {
            "form": form
        }
    )


# ==========================================================
# CUSTOM 404
# ==========================================================

def custom_404(request, exception):

    return render(
        request,
        "blog/404.html",
        status=404
    )


# ==========================================================
# CUSTOM 500
# ==========================================================

def custom_500(request):

    return render(
        request,
        "blog/500.html",
        status=500
    )

# ==========================================================
# AUTHOR PROFILE
# ==========================================================

def author_profile(request, username):

    author = get_object_or_404(
        User,
        username=username
    )

    posts = Post.objects.filter(
        author=author
    ).order_by("-created_at")

    return render(
        request,
        "blog/author_profile.html",
        {
            "author": author,
            "posts": posts,
        }
    )


# ==========================================================
# NEWSLETTER SUBSCRIBE
# ==========================================================

def newsletter(request):

    if request.method == "POST":

        form = NewsletterForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            if not Newsletter.objects.filter(email=email).exists():

                form.save()

                messages.success(
                    request,
                    "Thanks for subscribing!"
                )

            else:

                messages.info(
                    request,
                    "You are already subscribed."
                )

    return redirect("home")


# ==========================================================
# CONTACT FORM
# ==========================================================

def contact_form(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your message has been sent successfully."
            )

        else:

            messages.error(
                request,
                "Please correct the errors."
            )

    return redirect("contact")