from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Post, Category, Tag, Comment, Profile, Contact, Newsletter
from .forms import PostForm, CommentForm, UserRegisterForm, ProfileForm

class ModelTests(TestCase):
    """Test all models"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test description'
        )
        self.tag = Tag.objects.create(
            name='Test Tag',
            slug='test-tag'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            category=self.category,
            status='published',
            excerpt='Test excerpt'
        )
        self.post.tags.add(self.tag)
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment',
            active=True
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_tag_str(self):
        self.assertEqual(str(self.tag), 'Test Tag')

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_comment_str(self):
        self.assertEqual(str(self.comment), 'Comment by testuser on Test Post')

    def test_post_slug_auto_generated(self):
        post = Post.objects.create(
            title='Another Test Post',
            content='Content',
            author=self.user
        )
        self.assertEqual(post.slug, 'another-test-post')

    def test_post_views_increment(self):
        initial_views = self.post.views
        self.post.views += 1
        self.post.save()
        self.assertEqual(self.post.views, initial_views + 1)

    def test_post_total_likes(self):
        self.assertEqual(self.post.total_likes(), 0)
        self.post.likes.add(self.user)
        self.assertEqual(self.post.total_likes(), 1)

    def test_post_total_comments(self):
        self.assertEqual(self.post.total_comments(), 1)

    def test_comment_replies(self):
        reply = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test reply',
            parent=self.comment,
            active=True
        )
        self.assertEqual(self.comment.get_replies().count(), 1)

    def test_profile_created_for_user(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_contact_str(self):
        contact = Contact.objects.create(
            name='Test Name',
            email='test@test.com',
            subject='Test Subject',
            message='Test message'
        )
        self.assertEqual(str(contact), 'Test Name - Test Subject')

    def test_newsletter_str(self):
        newsletter = Newsletter.objects.create(email='test@test.com')
        self.assertEqual(str(newsletter), 'test@test.com')


class FormTests(TestCase):
    """Test all forms"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_post_form_valid_data(self):
        form = PostForm(data={
            'title': 'New Post',
            'content': 'This is test content for the post',
            'status': 'published'
        })
        self.assertTrue(form.is_valid())

    def test_post_form_invalid_title(self):
        form = PostForm(data={
            'title': 'Hi',
            'content': 'This is test content',
            'status': 'published'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_post_form_invalid_content(self):
        form = PostForm(data={
            'title': 'Test Title',
            'content': 'Short',
            'status': 'published'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_comment_form_valid(self):
        form = CommentForm(data={'content': 'This is a valid comment'})
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form = CommentForm(data={'content': 'Hi'})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_register_form_valid(self):
        form = UserRegisterForm(data={
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_username(self):
        form = UserRegisterForm(data={
            'username': 'ab',
            'email': 'new@test.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_register_form_invalid_email(self):
        form = UserRegisterForm(data={
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_profile_form_valid(self):
        form = ProfileForm(data={
            'username': 'testuser',
            'email': 'test@test.com',
            'bio': 'This is a test bio',
            'location': 'Test City',
        }, user=self.user)
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    """Test all views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.tag = Tag.objects.create(name='test-tag', slug='test-tag')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            category=self.category,
            status='published',
            excerpt='Test excerpt'
        )
        self.post.tags.add(self.tag)

    def test_home_page(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, 'Test Post')

    def test_post_detail_page(self):
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test content')

    def test_post_list_page(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_about_page(self):
        response = self.client.get(reverse('blog:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')

    def test_contact_page(self):
        response = self.client.get(reverse('blog:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/contact.html')

    def test_contact_form_submission(self):
        response = self.client.post(reverse('blog:contact'), {
            'name': 'Test User',
            'email': 'test@test.com',
            'subject': 'Test Subject',
            'message': 'This is a test message for contact form'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Contact.objects.filter(email='test@test.com').exists())

    def test_search_view(self):
        response = self.client.get(reverse('blog:search') + '?q=test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/search_results.html')
        self.assertContains(response, 'Test Post')

    def test_category_view(self):
        response = self.client.get(
            reverse('blog:category_posts', kwargs={'slug': self.category.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_posts.html')
        self.assertContains(response, 'Test Category')

    def test_tag_view(self):
        response = self.client.get(
            reverse('blog:tag_posts', kwargs={'slug': self.tag.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/tag_posts.html')
        self.assertContains(response, 'test-tag')

    def test_register_page(self):
        response = self.client.get(reverse('blog:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/register.html')

    def test_login_page(self):
        response = self.client.get(reverse('blog:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/login.html')

    def test_login_successful(self):
        response = self.client.post(reverse('blog:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('blog:home'))

    def test_login_failed(self):
        response = self.client.post(reverse('blog:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_register_successful(self):
        response = self.client.post(reverse('blog:register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertRedirects(response, reverse('blog:home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())


class AuthViewTests(TestCase):
    """Test authenticated views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            status='published'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_profile_view(self):
        response = self.client.get(reverse('blog:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/profile.html')
        self.assertContains(response, 'testuser')

    def test_dashboard_view(self):
        response = self.client.get(reverse('blog:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/dashboard.html')

    def test_create_post_view(self):
        response = self.client.get(reverse('blog:create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/create_post.html')

    def test_create_post_submission(self):
        response = self.client.post(reverse('blog:create_post'), {
            'title': 'New Test Post',
            'content': 'This is the content of the new test post',
            'status': 'published'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())

    def test_edit_post_view(self):
        response = self.client.get(
            reverse('blog:edit_post', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/edit_post.html')

    def test_edit_post_submission(self):
        response = self.client.post(
            reverse('blog:edit_post', kwargs={'slug': self.post.slug}),
            {
                'title': 'Updated Post Title',
                'content': 'Updated content',
                'status': 'published'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post Title')

    def test_delete_post_view(self):
        response = self.client.get(
            reverse('blog:delete_post', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/delete_post.html')

    def test_delete_post_submission(self):
        response = self.client.post(
            reverse('blog:delete_post', kwargs={'slug': self.post.slug})
        )
        self.assertRedirects(response, reverse('blog:profile'))
        self.assertFalse(Post.objects.filter(slug=self.post.slug).exists())

    def test_like_post(self):
        response = self.client.post(
            reverse('blog:like_post', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.total_likes(), 1)

    def test_unlike_post(self):
        self.post.likes.add(self.user)
        response = self.client.post(
            reverse('blog:like_post', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.total_likes(), 0)

    def test_bookmark_post(self):
        response = self.client.post(
            reverse('blog:bookmark_post', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertTrue(self.post.bookmarks.filter(id=self.user.id).exists())

    def test_unbookmark_post(self):
        self.post.bookmarks.add(self.user)
        response = self.client.post(
            reverse('blog:bookmark_post', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertFalse(self.post.bookmarks.filter(id=self.user.id).exists())


class APITests(TestCase):
    """Test API endpoints"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test API Post',
            content='Test content',
            author=self.user,
            status='published'
        )

    def test_search_autocomplete(self):
        response = self.client.get(
            reverse('blog:search_autocomplete') + '?q=test'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_post_stats_api(self):
        response = self.client.get(
            reverse('blog:post_stats_api', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], 'Test API Post')
        self.assertEqual(data['views'], 0)

    def test_recent_posts_api(self):
        response = self.client.get(reverse('blog:recent_posts_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_popular_posts_api(self):
        response = self.client.get(reverse('blog:popular_posts_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)


class MiddlewareTests(TestCase):
    """Test custom middleware"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_active_user_middleware(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        
        # Check if last_seen was updated
        user_profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(user_profile.last_seen)

    def test_security_headers(self):
        response = self.client.get(reverse('blog:home'))
        self.assertIn('X-Content-Type-Options', response)
        self.assertIn('X-Frame-Options', response)
        self.assertIn('X-XSS-Protection', response)


class SignalTests(TestCase):
    """Test Django signals"""
    
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(
            username='newuser',
            password='testpass123'
        )
        self.assertTrue(Profile.objects.filter(user=user).exists())