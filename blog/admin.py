from django.contrib import admin
from .models import Post, Category, Comment, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "category",
        "featured",
        "views",
        "created_at"
    )

    list_filter = (
        "featured",
        "category"
    )

    search_fields = (
        "title",
        "content"
    )
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Profile)