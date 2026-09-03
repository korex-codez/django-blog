from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os
import secrets
import random
import string


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short description of the post")
    featured_image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True, null=True)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)
    
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_posts', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # ========== NEW FIELDS ==========
    scheduled_publish = models.DateTimeField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['featured']),
            models.Index(fields=['scheduled_publish']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Make slug unique if it already exists
            if Post.objects.filter(slug=self.slug).exists():
                random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                self.slug = f"{self.slug}-{random_suffix}"
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
        
        if self.featured_image:
            self.optimize_image()

    def optimize_image(self):
        img_path = self.featured_image.path
        if os.path.exists(img_path):
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
            img.save(img_path, 'JPEG', quality=85, optimize=True)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def total_likes(self):
        # Optimization: Use annotated like_count if available to prevent N+1 queries during template rendering
        if hasattr(self, 'like_count'):
            return self.like_count
        return self.likes.count()

    def total_comments(self):
        return self.comments.filter(active=True).count()

    def get_next_post(self):
        return Post.objects.filter(
            status='published',
            published_at__gt=self.published_at
        ).order_by('published_at').first()

    def get_previous_post(self):
        return Post.objects.filter(
            status='published',
            published_at__lt=self.published_at
        ).order_by('-published_at').first()
    
    def track_view(self, request):
        """Track post view with IP and user agent"""
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create view record
        PostView.objects.create(
            post=self,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.views += 1
        self.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def get_replies(self):
        return self.replies.filter(active=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar and self.avatar != 'avatars/default.jpg':
            self.optimize_avatar()

    def optimize_avatar(self):
        img_path = self.avatar.path
        if os.path.exists(img_path):
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            size = (300, 300)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            width, height = img.size
            if width != height:
                new_size = min(width, height)
                left = (width - new_size) // 2
                top = (height - new_size) // 2
                img = img.crop((left, top, left + new_size, top + new_size))
                img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(img_path, 'JPEG', quality=85, optimize=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unsubscribe_token = models.CharField(max_length=100, blank=True, null=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email
    
    def generate_unsubscribe_token(self):
        self.unsubscribe_token = secrets.token_urlsafe(32)
        self.save()
        return self.unsubscribe_token
    
    def unsubscribe(self):
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()


# ========== NEW MODELS FOR ENHANCEMENTS ==========

class PostView(models.Model):
    """Track individual post views with IP and user agent"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='view_records')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
        verbose_name = 'Post View'
        verbose_name_plural = 'Post Views'

    def __str__(self):
        return f'{self.post.title} - {self.ip_address} - {self.viewed_at.strftime("%Y-%m-%d %H:%M")}'


class UserFollow(models.Model):
    """User following system"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']
        verbose_name = 'User Follow'
        verbose_name_plural = 'User Follows'

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'


class Activity(models.Model):
    """User activity feed"""
    ACTION_CHOICES = (
        ('post_created', 'Created a post'),
        ('post_updated', 'Updated a post'),
        ('comment_created', 'Commented on a post'),
        ('liked', 'Liked a post'),
        ('bookmarked', 'Bookmarked a post'),
        ('followed', 'Followed a user'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='targeted_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f'{self.user.username} - {self.get_action_display()} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'


# ==================== SIGNALS ====================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# ========== NEW SIGNALS ==========

@receiver(post_save, sender=Post)
def create_activity_on_post_creation(sender, instance, created, **kwargs):
    """Create activity when a post is created"""
    if created:
        Activity.objects.create(
            user=instance.author,
            action='post_created',
            post=instance
        )

@receiver(post_save, sender=Comment)
def create_activity_on_comment_creation(sender, instance, created, **kwargs):
    """Create activity when a comment is created"""
    if created:
        Activity.objects.create(
            user=instance.author,
            action='comment_created',
            post=instance.post,
            comment=instance
        )