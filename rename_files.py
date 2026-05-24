import os
import re

gallery_path = "static/gallery"

for filename in os.listdir(gallery_path):
    # Match pattern: "gallery (2).jpg" or "gallery (18).mp4"
    match = re.match(r'gallery \((\d+)\)\.(jpg|jpeg|png|mp4|webp)', filename)
    if match:
        number = match.group(1)
        extension = match.group(2)
        new_name = f"gallery-{number}.{extension}"

        old_path = os.path.join(gallery_path, filename)
        new_path = os.path.join(gallery_path, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_name}")

print("Done!")