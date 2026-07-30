from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListView, PostSitemap

app_name = 'blog'

urlpatterns = [
    # Core
    path('', views.home, name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    
    # Post CRUD - SPECIFIC FIRST
    path('post/create/', views.create_post, name='create_post'),
    path('post/edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('post/delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('post/like/<slug:slug>/', views.like_post, name='like_post'),
    path('post/bookmark/<slug:slug>/', views.bookmark_post, name='bookmark_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),  # CATCH-ALL LAST
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Profile - SPECIFIC FIRST
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),          # ⬅️ SPECIFIC
    path('profile/<str:username>/', views.profile_view, name='profile_view'), # ⬅️ CATCH-ALL
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Search & Filters
    path('search/', views.search_posts, name='search'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    
    # Static Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]

# Password Reset URLs
urlpatterns += [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='blog/password_reset.html',
             email_template_name='email/password_reset_email.html',
             subject_template_name='email/password_reset_subject.txt'
         ),
         name='password_reset'),  # ✅ This is why we use 'blog:password_reset'
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='blog/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='blog/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='blog/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]