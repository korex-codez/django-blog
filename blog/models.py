from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


# ==========================
# USER PROFILE
# ==========================

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="profiles/",
        default="profiles/default.png"
    )

    bio = models.TextField(
        blank=True,
        max_length=500
    )

    website = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username


# ==========================
# CATEGORY
# ==========================

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# ==========================
# BLOG POST
# ==========================

class Post(models.Model):

    title = models.CharField(
        max_length=200
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    content = RichTextField()

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True
    )

    views = models.PositiveIntegerField(
        default=0
    )

    featured = models.BooleanField(
        default=False
    )

    likes = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True
    )

    bookmarks = models.ManyToManyField(
        User,
        related_name="bookmarked_posts",
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "post_detail",
            args=[self.id]
        )

    @property
    def reading_time(self):
        words = len(self.content.split())
        return max(1, words // 200)

    def total_likes(self):
        return self.likes.count()


# ==========================
# COMMENTS
# ==========================

class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = RichTextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


# ==========================
# NEWSLETTER
# ==========================

class Newsletter(models.Model):

    email = models.EmailField(
        unique=True
    )

    subscribed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.email


# ==========================
# CONTACT MESSAGES
# ==========================

class Contact(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.subject