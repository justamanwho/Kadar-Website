import os
from PIL import Image
import re

def optimize_image(image_path, max_width=1920, quality=85):
    with Image.open(image_path) as img:
        # Resize if too large
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # Convert to WebP if supported
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            webp_path = os.path.splitext(image_path)[0] + '.webp'
            img.save(webp_path, 'WEBP', quality=quality, optimize=True)
        else:
            img.save(image_path, optimize=True, quality=quality)


def optimize_all_images():
    for root, dirs, files in os.walk('static'):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                optimize_image(os.path.join(root, file))


def safe_minify(css):
    # Remove comments but preserve important animations
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)

    # Collapse whitespace but be careful with calc() functions
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r';\s*', ';', css)
    css = re.sub(r':\s*', ':', css)
    css = re.sub(r'\s*{\s*', '{', css)
    css = re.sub(r'\s*}\s*', '}', css)
    css = re.sub(r',\s*', ',', css)

    return css.strip()


def compress_slider_images():
    for i in range(1, 6):
        input_path = f"static/slides/horizontal{i}.jpg"
        output_path = f"static/slides/horizontal{i}.webp"

        with Image.open(input_path) as img:
            if img.width > 1920:
                ratio = 1920 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((1920, new_height), Image.Resampling.LANCZOS)

            # Save as WebP with 75% quality
            img.save(output_path, 'WEBP', quality=75, optimize=True)

        print(f"Compressed: {input_path} -> {output_path}")


def compress_more():
    for i in range(1, 6):
        input_path = f"static/slides/horizontal{i}.jpg"
        output_path = f"static/slides/horizontal{i}.webp"

        with Image.open(input_path) as img:
            # Resize to exactly 1920px width
            if img.width != 1920:
                ratio = 1920 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((1920, new_height), Image.Resampling.LANCZOS)

            # Lower quality to 70%
            img.save(output_path, 'WEBP', quality=70, method=6)  # method=6 for best compression

        print(f"Re-compressed: {output_path}")


if __name__ == '__main__':
    # optimize_all_images()
    # compress_slider_images()
    # compress_more()

    # Read your original CSS
    with open('static/styles.css', 'r', encoding='utf-8') as f:
        original = f.read()

    # Minify safely
    fixed_css = safe_minify(original)

    # Save new minified version
    with open('static/styles.min.css', 'w', encoding='utf-8') as f:
        f.write(fixed_css)

    print("Fixed minified CSS created!")