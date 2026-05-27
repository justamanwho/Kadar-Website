import os
import subprocess
from PIL import Image


# =========================
# IMAGE OPTIMIZATION
# =========================
def optimize_image(image_path, max_width=1920, quality=85, delete_original=False):
    try:
        with Image.open(image_path) as img:
            # Resize if too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Convert to WebP
            webp_path = os.path.splitext(image_path)[0] + '.webp'
            img.save(webp_path, 'WEBP', quality=quality, optimize=True)

        print(f"Image optimized: {image_path}")

        # Optionally delete original
        if delete_original and os.path.exists(webp_path):
            os.remove(image_path)

    except Exception as e:
        print(f"Image error ({image_path}): {e}")


# =========================
# VIDEO OPTIMIZATION
# =========================
def optimize_video(video_path):
    try:
        # Avoid recompressing
        if "_compressed" in video_path:
            return

        output_path = os.path.splitext(video_path)[0] + "_compressed.mp4"

        command = [
            "ffmpeg",
            "-y",  # overwrite
            "-i", video_path,
            "-vcodec", "libx264",
            "-crf", "28",
            "-preset", "slow",
            "-acodec", "aac",
            "-b:a", "128k",
            output_path
        ]

        subprocess.run(command, check=True)
        print(f"Video compressed: {video_path}")

    except Exception as e:
        print(f"Video error ({video_path}): {e}")


# =========================
# MEDIA PIPELINE
# =========================
def optimize_all_media(folder="static"):
    for root, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            lower = file.lower()

            if lower.endswith(('.png', '.jpg', '.jpeg')):
                optimize_image(path)

            elif lower.endswith(('.mp4', '.mov', '.webm')):
                optimize_video(path)



if __name__ == '__main__':
    optimize_all_media("static")

