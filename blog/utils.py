from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from PIL import Image
import os
import re
from datetime import datetime, timedelta

def send_email_notification(subject, template, context, recipient_list):
    """Send email notification using template"""
    try:
        html_message = render_to_string(template, context)
        plain_message = render_to_string(template.replace('.html', '.txt'), context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def optimize_image(image_path, max_size=(1200, 800), quality=85):
    """Optimize image size and quality"""
    try:
        if os.path.exists(image_path):
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if larger than max_size
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
            return True
    except Exception as e:
        print(f"Failed to optimize image: {e}")
        return False

def generate_slug(text, model, slug_field='slug'):
    """Generate unique slug for model"""
    from django.utils.text import slugify
    import uuid
    
    base_slug = slugify(text)
    slug = base_slug
    
    # Check if slug exists
    queryset = model.objects.filter(**{slug_field: slug})
    counter = 1
    while queryset.exists():
        slug = f"{base_slug}-{counter}"
        queryset = model.objects.filter(**{slug_field: slug})
        counter += 1
    
    return slug

def extract_hashtags(text):
    """Extract hashtags from text"""
    return re.findall(r'#(\w+)', text)

def get_read_time(html_content):
    """Calculate reading time in minutes"""
    if not html_content:
        return 1
    
    # Remove HTML tags
    plain_text = re.sub(r'<[^>]*>', ' ', html_content)
    # Remove extra whitespace
    plain_text = re.sub(r'\s+', ' ', plain_text).strip()
    # Count words
    words = len(plain_text.split())
    # Average reading speed: 200 words per minute
    minutes = max(1, round(words / 200))
    
    return minutes

def get_today_date():
    """Get today's date"""
    return timezone.now().date()

def get_week_range():
    """Get start and end of current week"""
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def get_month_range():
    """Get start and end of current month"""
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    if today.month == 12:
        end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    return start_of_month, end_of_month

def format_number(num):
    """Format number with K, M, B suffixes"""
    if not num:
        return '0'
    
    num = float(num)
    if num >= 1_000_000_000:
        return f'{num/1_000_000_000:.1f}B'
    elif num >= 1_000_000:
        return f'{num/1_000_000:.1f}M'
    elif num >= 1000:
        return f'{num/1000:.1f}K'
    else:
        return str(int(num))

def get_user_ip(request):
    """Get user IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_device(request):
    """Detect user device type from user agent"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    
    if 'mobile' in user_agent:
        return 'mobile'
    elif 'tablet' in user_agent:
        return 'tablet'
    else:
        return 'desktop'