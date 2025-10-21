import time
import glob
from typing import Any, Dict
import ray

from application.services.photo import ImageResizer, JPGResizer


SOURCE_DIR = "source_images"


@ray.remote
class ImageProcessorActor:
    def __init__(self):
        self.status = "IDLE"
        self.processed_count = 0
        self.total_count = 0
        self.last_run_time = 0
        
    def get_status(self) -> Dict[str, Any]:
        """Returns the current status of the actor."""
        
        return {
            "status": self.status,
            "processed_count": self.processed_count,
            "total_count": self.total_count,
            "last_run_time_seconds": round(self.last_run_time, 2)
        }
        
    async def process_batch(self, photo_path: str) -> Dict[str, Any]:
        """
        This actor handler for all resizing tasks.
        
        """
        if self.status == "PROCESSING":
            return {"message": "Job is already in progress."}

        print("Actor: Starting batch process...")
        self.status = "PROCESSING"
        
        start_time = time.time()
        
        image_paths = glob.glob(f"{SOURCE_DIR}/*.jpg")
        self.total_count = len(image_paths)
        self.processed_count = 0
        
        if not image_paths:
            self.status = "IDLE"
            return {"message": "No images found to process."}


        futures = [ImageResizer(JPGResizer).resize_images.remote(path) for path in image_paths]
        
        results = ray.get(futures)
        
        self.processed_count = len(results)
        self.status = "COMPLETED"
        self.last_run_time = time.time() - start_time
        
        print(f"Actor: Batch complete in {self.last_run_time:.2f}s")
        return {
            "message": "Batch processing complete.",
            "count": self.processed_count,
            "time": self.last_run_time
        }
    