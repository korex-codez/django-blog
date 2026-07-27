from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Separate tags with commas"
    )
    bookmarks = models.ManyToManyField(
        User,
        related_name="bookmarked_posts",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def reading_time(self):
        words = len(self.content.split())
        minutes = words // 200
        if minutes < 1:
            minutes = 1
        return minutes

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profiles/", default="profiles/default.png")
    bio = models.TextField(blank=True)