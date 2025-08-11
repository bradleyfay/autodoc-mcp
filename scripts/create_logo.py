#!/usr/bin/env python3
"""
AutoDocs Logo Creation Script

Creates professional logo.png (512x512) and favicon.ico for AutoDocs MCP Server.
Uses Python PIL for high-quality graphics generation.
"""

import os

from PIL import Image, ImageDraw, ImageFont


def create_logo():
    """Create a professional AutoDocs logo."""
    # Create 512x512 canvas with white background
    img = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Define colors matching the blue theme from mkdocs.yml
    primary_blue = (37, 99, 235)  # #2563eb
    dark_blue = (30, 64, 175)  # #1e40af
    light_blue = (96, 165, 250)  # #60a5fa
    white = (255, 255, 255)

    # Create rounded rectangle background with gradient effect
    # Main background shape
    draw.rounded_rectangle([(64, 64), (448, 448)], radius=32, fill=primary_blue)

    # Add subtle gradient effect with overlay
    draw.rounded_rectangle([(64, 64), (448, 320)], radius=32, fill=None, outline=None)

    # Overlay for gradient effect
    overlay = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Create gradient by drawing multiple rectangles with increasing transparency
    for i in range(128):
        alpha = int(20 * (1 - i / 128))
        color = (*dark_blue, alpha)
        y_start = 64 + i * 2
        if y_start < 320:
            overlay_draw.rounded_rectangle(
                [(64, y_start), (448, y_start + 2)], radius=32, fill=color
            )

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Try to use a system font, fall back to default if not available
    try:
        # Try different font locations for cross-platform compatibility
        font_paths = [
            "/System/Library/Fonts/SF-Pro-Display-Bold.otf",  # macOS
            "/System/Library/Fonts/Helvetica.ttc",  # macOS fallback
            "C:/Windows/Fonts/segoeui.ttf",  # Windows
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
        ]

        main_font = None
        sub_font = None
        small_font = None

        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    main_font = ImageFont.truetype(font_path, 84)
                    sub_font = ImageFont.truetype(font_path, 36)
                    small_font = ImageFont.truetype(font_path, 28)
                    break
                except Exception:
                    continue

        # If no system fonts found, use default
        if not main_font:
            main_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

    except Exception:
        # Fallback to default font
        main_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw main "AD" monogram
    bbox = draw.textbbox((0, 0), "AD", font=main_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (512 - text_width) // 2
    y = 180 - text_height // 2

    # Add subtle shadow
    draw.text((x + 2, y + 2), "AD", font=main_font, fill=(0, 0, 0, 60))
    # Main text
    draw.text((x, y), "AD", font=main_font, fill=white)

    # Draw "AUTO DOCS" text
    bbox = draw.textbbox((0, 0), "AUTO DOCS", font=sub_font)
    text_width = bbox[2] - bbox[0]
    x = (512 - text_width) // 2
    y = 280

    draw.text((x + 1, y + 1), "AUTO DOCS", font=sub_font, fill=(0, 0, 0, 60))
    draw.text((x, y), "AUTO DOCS", font=sub_font, fill=white)

    # Draw decorative line
    draw.line([(128, 340), (384, 340)], fill=light_blue, width=3)

    # Add small dots for decoration
    for i in range(3):
        x_dot = 220 + i * 24
        draw.ellipse([(x_dot, 350), (x_dot + 8, 358)], fill=light_blue)

    # Draw "MCP Server" subtitle
    bbox = draw.textbbox((0, 0), "MCP Server", font=small_font)
    text_width = bbox[2] - bbox[0]
    x = (512 - text_width) // 2
    y = 380

    draw.text((x + 1, y + 1), "MCP Server", font=small_font, fill=(0, 0, 0, 60))
    draw.text((x, y), "MCP Server", font=small_font, fill=light_blue)

    return img


def create_favicon(logo_img):
    """Create favicon.ico from logo image."""
    # Create multiple sizes for favicon
    sizes = [16, 32, 48, 64, 128, 256]
    favicon_images = []

    for size in sizes:
        favicon_img = logo_img.resize((size, size), Image.Resampling.LANCZOS)
        favicon_images.append(favicon_img)

    return favicon_images


def main():
    """Main function to create logo and favicon."""
    print("Creating AutoDocs logo and favicon...")

    # Ensure docs/assets directory exists
    assets_dir = "/Users/bradleyfay/autodocs/docs/assets"
    os.makedirs(assets_dir, exist_ok=True)

    # Create logo
    logo = create_logo()

    # Save logo as PNG
    logo_path = os.path.join(assets_dir, "logo.png")
    logo.save(logo_path, "PNG", optimize=True)
    print(f"✅ Logo saved: {logo_path}")

    # Create and save favicon
    favicon_images = create_favicon(logo)
    favicon_path = os.path.join(assets_dir, "favicon.ico")

    # Save as ICO with multiple sizes
    favicon_images[0].save(
        favicon_path,
        format="ICO",
        sizes=[(img.width, img.height) for img in favicon_images],
        append_images=favicon_images[1:],
    )
    print(f"✅ Favicon saved: {favicon_path}")

    print("\n🎨 Professional assets created successfully!")
    print(f"   Logo: {logo_path} (512x512 PNG)")
    print(f"   Favicon: {favicon_path} (Multi-size ICO)")
    print("\nAssets are optimized and ready for production use.")


if __name__ == "__main__":
    main()
