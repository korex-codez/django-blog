from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Category, Tag

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('blog:post_detail', kwargs={'slug': obj.slug})

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class TagSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Tag.objects.all()

class StaticViewSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.4

    def items(self):
        return ['blog:home', 'blog:about', 'blog:contact']

    def location(self, item):
        return reverse(item)