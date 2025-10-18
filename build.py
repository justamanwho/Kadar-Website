import os
from PIL import Image
from cssmin import cssmin

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

def minify_all_css():
    css_files = ['static/styles.css']
    for css_file in css_files:
        with open(css_file, 'r') as f:
            minified = cssmin(f.read())
        with open(css_file.replace('.css', '.min.css'), 'w') as f:
            f.write(minified)

if __name__ == '__main__':
    optimize_all_images()
    minify_all_css()