"""
Custom ThumborStorage class to override image saving behavior.

This class extends the BaseStorage class provided by Thumbor to customize the image
saving process. The original ThumborStorage validates the file name before saving,
but we want to override this behavior.

Example usage:
    storage = CustomThumborStorage()
    storage.save('path/to/image.jpg', image_bytes)
"""

import os
from thumbor.storages import BaseStorage
from django.conf import settings

class CustomThumborStorage(BaseStorage):
    def save(self, path, bytes):
        """
        Save the image bytes without calling validate_file_name().

        Args:
            path (str): The path where the image should be saved.
            bytes (bytes): The image bytes to be saved.
        Returns:
            str: The saved image path.
        """
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        with open(file_path, 'wb') as f:
            f.write(bytes)

        return path
