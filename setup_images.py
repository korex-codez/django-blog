import os
from PIL import Image, ImageDraw, ImageFont

def create_default_avatar():
    """Create default avatar using PIL"""
    size = 300
    img = Image.new('RGB', (size, size), '#2563eb')
    draw = ImageDraw.Draw(img)
    
    # Draw circle background
    draw.ellipse([(0, 0), (size, size)], fill='#3b82f6')
    
    # Draw user icon (head)
    draw.ellipse([(size//2 - 50, 60), (size//2 + 50, 160)], fill='white')
    
    # Draw user icon (body)
    draw.ellipse([(size//2 - 70, 200), (size//2 + 70, 300)], fill='white')
    
    # Save
    os.makedirs('media/avatars', exist_ok=True)
    img.save('media/avatars/default.jpg', 'JPEG', quality=95)
    print("✅ Default avatar created!")

def create_og_image():
    """Create Open Graph image using PIL"""
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), '#0f172a')
    draw = ImageDraw.Draw(img)
    
    # Gradient effect - draw rectangles
    for i in range(0, height, 10):
        alpha = int(50 + (i / height) * 50)
        draw.rectangle([(0, i), (width, i+10)], fill=f'#{alpha:02x}3b82f6')
    
    # Draw blog icon (circle with B)
    cx, cy = 200, 315
    draw.ellipse([(cx-70, cy-70), (cx+70, cy+70)], fill='#2563eb')
    
    # Draw B letter using PIL
    try:
        # Try to use a system font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        try:
            # Fallback for Windows
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            # Fallback to default
            font = ImageFont.load_default()
    
    draw.text((150, 280), "PixelPost", fill='white', font=font)
    draw.text((150, 350), "Professional Blog about Technology & Development", fill='#94a3b8', font=font)
    
    os.makedirs('static/img', exist_ok=True)
    img.save('static/img/og-image.jpg', 'JPEG', quality=95)
    print("✅ OG Image created!")

def create_hero_illustration():
    """Create simple hero illustration"""
    print("✅ Hero illustration SVG is ready!")
    print("   Use the hero-illustration.svg file provided.")

def main():
    print("🔄 Creating images...")
    print("-" * 40)
    
    create_default_avatar()
    create_og_image()
    create_hero_illustration()
    
    print("-" * 40)
    print("✅ All images created successfully!")
    print("\n📁 Image locations:")
    print("   - media/avatars/default.jpg")
    print("   - static/img/og-image.jpg")

if __name__ == '__main__':
    main()