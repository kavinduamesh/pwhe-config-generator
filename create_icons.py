#!/usr/bin/env python3
"""
PWA Icon Generator for PW-HE Config Generator
This script creates all the required icon sizes for PWA installation.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, text="PWHE"):
    """Create a simple icon with text."""
    # Create a new image with the specified size
    img = Image.new('RGBA', (size, size), (103, 80, 164, 255))  # Material 3 primary color
    
    # Create a drawing object
    draw = ImageDraw.Draw(img)
    
    # Calculate font size (approximately 1/3 of the image size)
    font_size = max(12, size // 3)
    
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    # Calculate text position to center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Draw the text
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    return img

def main():
    """Generate all required icon sizes."""
    # Create icons directory if it doesn't exist
    icons_dir = "public/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Required icon sizes for PWA
    sizes = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512]
    
    print("Creating PWA icons...")
    
    for size in sizes:
        icon = create_icon(size)
        filename = f"{icons_dir}/icon-{size}x{size}.png"
        icon.save(filename, "PNG")
        print(f"Created: {filename}")
    
    print("\nAll icons created successfully!")
    print(f"Icons saved in: {icons_dir}")
    print("\nNext steps:")
    print("1. Deploy your app to hosting (Render, Firebase, etc.)")
    print("2. Open in Chrome/Edge")
    print("3. Click the install button in the address bar")
    print("4. Your app will be installed as a Windows desktop app!")

if __name__ == "__main__":
    main()

