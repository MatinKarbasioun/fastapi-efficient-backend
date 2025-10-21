from PIL import Image

import ray

THUMB_DIR = "thumbnail_images"
THUMB_SIZE = (128, 128)


class ImageResizer:
    def __init__(self, image_resizer: 'ImageResizer'):
        self._resizer = image_resizer
        
    @ray.remote
    def resize_images(self, image_path):
        """Ray task to resize a single image with different format"""
        
        return self._resizer.resize_images(image_path)
    
    
class JPGResizer(ImageResizer):
    
    @classmethod
    def resize_images(cls, image_path: str):
        
        
        try:
            from PIL import Image 
            import os
            
            
            img_name = os.path.basename(image_path)
            target_path = os.path.join(THUMB_DIR, img_name)
            
            if os.path.exists(target_path):
                return f"Skipped (already exists): {img_name}"
            
            img = Image.open(image_path)
            img.thumbnail(THUMB_SIZE)
            img.save(target_path)
            return f"Processed: {img_name}"
        
        except Exception as e:
            return f"Failed {img_name}: {e}"

