from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment
from django.utils.text import slugify
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample data (No Faker required)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--posts',
            type=int,
            default=20,
            help='Number of posts to create',
        )
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of users to create',
        )

    def generate_random_text(self, min_words=5, max_words=20):
        """Generate random text without Faker"""
        words = [
            'technology', 'programming', 'development', 'software', 'coding',
            'python', 'django', 'javascript', 'react', 'database', 'cloud',
            'api', 'server', 'client', 'web', 'mobile', 'desktop', 'framework',
            'library', 'tool', 'platform', 'system', 'network', 'security',
            'data', 'analysis', 'machine', 'learning', 'artificial', 'intelligence',
            'blockchain', 'crypto', 'web3', 'metaverse', 'devops', 'agile',
            'scrum', 'kanban', 'git', 'github', 'testing', 'deployment'
        ]
        
        num_words = random.randint(min_words, max_words)
        return ' '.join(random.choices(words, k=num_words))

    def handle(self, *args, **options):
        num_posts = options['posts']
        num_users = options['users']
        
        self.stdout.write('🔄 Creating sample data...')
        
        # Create categories
        categories = [
            'Technology', 'Programming', 'Web Development', 
            'Data Science', 'Artificial Intelligence', 'Cloud Computing',
            'DevOps', 'Cybersecurity', 'Machine Learning', 'Python',
            'JavaScript', 'React', 'Django', 'Flask', 'Database'
        ]
        
        category_objs = []
        for cat in categories:
            obj, created = Category.objects.get_or_create(
                name=cat,
                defaults={'slug': slugify(cat)}
            )
            category_objs.append(obj)
        self.stdout.write(f'✅ Created {len(category_objs)} categories')
        
        # Create tags
        tags = [
            'Python', 'JavaScript', 'React', 'Django', 'Flask',
            'Machine Learning', 'AI', 'Cloud', 'AWS', 'Docker',
            'Kubernetes', 'Git', 'Linux', 'API', 'GraphQL'
        ]
        
        tag_objs = []
        for tag in tags:
            obj, created = Tag.objects.get_or_create(
                name=tag,
                defaults={'slug': slugify(tag)}
            )
            tag_objs.append(obj)
        self.stdout.write(f'✅ Created {len(tag_objs)} tags')
        
        # Create users
        users = []
        for i in range(num_users):
            username = f'user_{i+1}'
            email = f'user{i+1}@example.com'
            password = 'password123'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_active': True
                }
            )
            if created:
                user.set_password(password)
                user.save()
                user.profile.bio = f'This is the bio of {username}'
                user.profile.location = f'City {i+1}'
                user.profile.occupation = random.choice(['Developer', 'Designer', 'Manager', 'Student'])
                user.profile.save()
                self.stdout.write(f'✅ Created user: {username}')
            users.append(user)
        
        # Create posts
        post_count = 0
        for i in range(num_posts):
            title = self.generate_random_text(3, 8).title()
            content_parts = []
            for j in range(random.randint(3, 8)):
                content_parts.append(self.generate_random_text(10, 30))
            content = '\n\n'.join(content_parts)
            excerpt = self.generate_random_text(5, 15)
            
            author = random.choice(users)
            category = random.choice(category_objs)
            status = random.choice(['draft', 'published', 'published', 'published'])
            
            post = Post.objects.create(
                title=title,
                content=content,
                excerpt=excerpt,
                author=author,
                category=category,
                status=status,
                featured=random.choice([True, False]),
                views=random.randint(0, 1000)
            )
            
            # Add tags
            num_tags = random.randint(2, min(5, len(tag_objs)))
            post.tags.add(*random.sample(tag_objs, num_tags))
            
            # Add comments
            num_comments = random.randint(0, 10)
            for j in range(num_comments):
                comment_content = self.generate_random_text(3, 10)
                Comment.objects.create(
                    post=post,
                    author=random.choice(users),
                    content=comment_content,
                    active=random.choice([True, True, True, False])
                )
            
            post_count += 1
            if post_count % 5 == 0:
                self.stdout.write(f'   Created {post_count} posts...')
        
        self.stdout.write(self.style.SUCCESS(f'✅ Successfully seeded database with {num_posts} posts, {num_users} users'))