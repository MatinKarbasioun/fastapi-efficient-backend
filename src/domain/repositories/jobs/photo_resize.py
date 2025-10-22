from abc import ABC, abstractmethod


class IPhotoResizeRepository(ABC):
    
    @abstractmethod
    def dispatch_image_processing(self, image_id: int):
        """Sends a job to process the image."""
        raise NotImplementedError