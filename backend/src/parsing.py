import zipfile
from PIL import Image
from io import BytesIO
import os

def extract_cover_image(epub_path):
    with zipfile.ZipFile(epub_path, 'r') as z:
        # List all files in the EPUB zip
        for file_info in z.infolist():
            # Look for common locations of cover images in EPUB files
            if "cover" in file_info.filename.lower() and file_info.filename.endswith(('.jpg', '.jpeg', '.png')):
                with z.open(file_info) as image_file:
                    image = Image.open(BytesIO(image_file.read()))
                    cover_image_path = epub_path.replace(".epub", ".jpg")
                    image.save(cover_image_path)
                    return cover_image_path
    return None