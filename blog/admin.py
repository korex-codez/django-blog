from django.contrib import admin
from .models import (
    Profile,
    Category,
    Post,
    Comment,
    Newsletter,
    Contact,
)


# ==========================================================
# PROFILE
# ==========================================================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "created_at",
    )

    search_fields = (
        "user__username",
    )


# ==========================================================
# CATEGORY
# ==========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )


# ==========================================================
# POST
# ==========================================================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "category",
        "featured",
        "views",
        "created_at",
    )

    list_filter = (
        "featured",
        "category",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
        "author__username",
    )

    filter_horizontal = (
        "likes",
        "bookmarks",
    )


# ==========================================================
# COMMENT
# ==========================================================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "post",
        "created_at",
    )

    search_fields = (
        "user__username",
        "post__title",
    )


# ==========================================================
# NEWSLETTER
# ==========================================================

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "subscribed_at",
    )

    search_fields = (
        "email",
    )


# ==========================================================
# CONTACT
# ==========================================================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
    )