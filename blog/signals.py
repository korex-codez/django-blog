from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Post, Newsletter
import os

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.status == 'published':
        subscribers = Newsletter.objects.filter(is_active=True)
        if subscribers.exists():
            # Prepare email list
            emails = []
            for subscriber in subscribers:
                # Generate unsubscribe token if not exists
                if not subscriber.unsubscribe_token:
                    subscriber.generate_unsubscribe_token()
                
                context = {
                    'subscriber_name': subscriber.email.split('@')[0],
                    'subscriber_email': subscriber.email,
                    'post': instance,
                    'protocol': 'https' if not settings.DEBUG else 'http',
                    'domain': settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost:8000',
                }
                
                subject = f"New Post: {instance.title}"
                html_message = render_to_string('email/newsletter_email.html', {
                    **context,
                    'subject': subject,
                    'intro_message': f"A new post has been published on our blog:",
                    'posts': [instance],
                })
                plain_message = f"""
                New Post: {instance.title}
                
                By: {instance.author.username}
                Published: {instance.created_at.strftime('%B %d, %Y')}
                
                {instance.excerpt}
                
                Read the full post: {context['protocol']}://{context['domain']}{instance.get_absolute_url()}
                
                To unsubscribe: {context['protocol']}://{context['domain']}/newsletter/unsubscribe/?email={subscriber.email}&token={subscriber.unsubscribe_token}
                """
                
                emails.append((
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    html_message,
                ))
            
            try:
                # Send emails in batches
                for email in emails:
                    send_mail(
                        email[0],
                        email[1],
                        email[2],
                        email[3],
                        fail_silently=True,
                        html_message=email[4],
                    )
            except Exception as e:
                print(f"Failed to send newsletter: {e}")