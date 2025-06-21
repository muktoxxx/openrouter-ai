import os
import uuid
from PIL import Image
import io
from typing import Tuple, Optional
import requests
from config import Config

class ImageProcessor:
    def __init__(self):
        self.temp_dir = os.path.join("static", "temp_images")
        os.makedirs(self.temp_dir, exist_ok=True)

    def save_image_from_file(self, file) -> Tuple[str, bool]:
        """Save an image from Telegram file to temp storage"""
        try:
            image_path = os.path.join(self.temp_dir, f"{uuid.uuid4()}.jpg")
            file.save(image_path)
            return image_path, True
        except Exception as e:
            print(f"Error saving image: {e}")
            return "", False

    def save_image_from_url(self, url: str) -> Tuple[str, bool]:
        """Download and save image from URL"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            image_path = os.path.join(self.temp_dir, f"{uuid.uuid4()}.jpg")
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return image_path, True
        except Exception as e:
            print(f"Error downloading image: {e}")
            return "", False

    def get_pillow_image(self, image_path: str) -> Optional[Image.Image]:
        """Load image using PIL"""
        try:
            return Image.open(image_path)
        except Exception as e:
            print(f"Error opening image: {e}")
            return None

    def clean_temp_images(self):
        """Clean up temporary image files"""
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")