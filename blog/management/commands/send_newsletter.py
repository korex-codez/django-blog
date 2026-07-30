from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from blog.models import Post, Newsletter
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Send weekly newsletter to subscribers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--weeks',
            type=int,
            default=1,
            help='Number of weeks to look back for posts',
        )

    def handle(self, *args, **options):
        weeks = options['weeks']
        cutoff_date = datetime.now() - timedelta(weeks=weeks)
        
        # Get recent posts
        posts = Post.objects.filter(
            status='published',
            published_at__gte=cutoff_date
        ).order_by('-published_at')[:10]
        
        if not posts:
            self.stdout.write('No new posts found.')
            return
        
        # Get active subscribers
        subscribers = Newsletter.objects.filter(is_active=True)
        
        if not subscribers.exists():
            self.stdout.write('No subscribers found.')
            return
        
        # Prepare and send emails
        for subscriber in subscribers:
            if not subscriber.unsubscribe_token:
                subscriber.generate_unsubscribe_token()
            
            context = {
                'subscriber_name': subscriber.email.split('@')[0],
                'subscriber_email': subscriber.email,
                'posts': posts,
                'protocol': 'https' if not settings.DEBUG else 'http',
                'domain': settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost:8000',
                'subject': f'Weekly Newsletter - {datetime.now().strftime("%B %d, %Y")}',
                'intro_message': "Here are the latest posts from our blog:",
            }
            
            html_message = render_to_string('email/newsletter_email.html', context)
            plain_message = f"""
            Weekly Newsletter
            
            Here are the latest posts from our blog:
            
            {chr(10).join([f'- {post.title} by {post.author.username}' for post in posts])}
            
            Visit our blog: {context['protocol']}://{context['domain']}
            
            To unsubscribe: {context['protocol']}://{context['domain']}/newsletter/unsubscribe/?email={subscriber.email}&token={subscriber.unsubscribe_token}
            """
            
            try:
                send_mail(
                    context['subject'],
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    fail_silently=True,
                    html_message=html_message,
                )
                self.stdout.write(f'Newsletter sent to {subscriber.email}')
            except Exception as e:
                self.stderr.write(f'Failed to send to {subscriber.email}: {e}')
        
        self.stdout.write(self.style.SUCCESS('Newsletter sent successfully!'))