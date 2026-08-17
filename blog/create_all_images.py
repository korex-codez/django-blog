"""
Run this script to create all required images for your blog.
Make sure Pillow is installed: pip install Pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_favicon():
    """Create favicon.ico"""
    size = 32
    img = Image.new('RGB', (size, size), '#2563eb')
    draw = ImageDraw.Draw(img)
    
    # Simple B letter
    draw.text((8, 0), "B", fill='white')
    
    os.makedirs('static/img', exist_ok=True)
    img.save('static/img/favicon.ico', format='ICO')
    print("✅ Favicon created!")

def create_hero_svg():
    """Hero illustration is provided as SVG"""
    print("✅ Hero illustration SVG provided.")
    print("   Copy hero-illustration.svg to static/img/")

def create_og_image():
    """Create OG image with better quality"""
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), '#0f172a')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background
    for i in range(height):
        r = int(20 + (i / height) * 30)
        g = int(20 + (i / height) * 40)
        b = int(50 + (i / height) * 60)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Draw main circle
    cx, cy = 200, 315
    draw.ellipse([(cx-70, cy-70), (cx+70, cy+70)], fill='#2563eb')
    
    # Try to use a font, fallback to default
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw text
    draw.text((300, 280), "PixelPost", fill='white', font=font_big)
    draw.text((300, 350), "Professional Blog about Technology & Development", fill='#94a3b8', font=font_small)
    
    # Draw decorative line
    draw.line([(300, 250), (450, 250)], fill='#3b82f6', width=4)
    
    # Draw code blocks on the right
    for i, y in enumerate([180, 230, 280, 330, 380, 430]):
        x = 700
        width_block = 350 if i % 2 == 0 else 280
        height_block = 30
        draw.rectangle([(x, y), (x + width_block, y + height_block)], 
                      fill=(30, 41, 59), outline=(51, 65, 85))
    
    os.makedirs('static/img', exist_ok=True)
    img.save('static/img/create_og_image.html', 'JPEG', quality=95)
    print("✅ OG Image created!")

def create_default_avatar():
    """Create default avatar"""
    size = 300
    img = Image.new('RGB', (size, size), '#2563eb')
    draw = ImageDraw.Draw(img)
    
    # Background circle with gradient
    for i in range(size):
        color = int(30 + (i / size) * 50)
        draw.line([(0, i), (size, i)], fill=(color, 90 + color//2, 200))
    
    # User head
    draw.ellipse([(size//2 - 50, 60), (size//2 + 50, 160)], fill='white')
    
    # User body
    draw.ellipse([(size//2 - 70, 200), (size//2 + 70, 300)], fill='white')
    
    os.makedirs('media/avatars', exist_ok=True)
    img.save('media/avatars/default.jpg', 'JPEG', quality=95)
    print("✅ Default avatar created!")

def main():
    print("🔄 Creating all images...")
    print("-" * 40)
    
    create_favicon()
    create_hero_svg()
    create_og_image()
    create_default_avatar()
    
    print("-" * 40)
    print("✅ All images created successfully!")
    print("\n📁 Image locations:")
    print("   - static/img/favicon.ico")
    print("   - static/img/hero-illustration.svg")
    print("   - static/img/create_og_image.html")
    print("   - media/avatars/default.jpg")

if __name__ == '__main__':
    main()