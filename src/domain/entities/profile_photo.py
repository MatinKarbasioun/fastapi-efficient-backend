from dataclasses import dataclass, field
import datetime
from typing import Optional

from domain.value_objects.image_status import ImageStatus


@dataclass(frozen=False)
class ProfilePhoto:
    """ User profile image entity """
    id: Optional[int]
    user_id: int
    original_url: str
    is_active: bool
    thumb_url: Optional[str]
    medium_url: Optional[str]
    state: ImageStatus = ImageStatus.PROCESSING
    created_at: Optional[datetime.datetime] = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    def mark_as_completed(self, thumb_path: str, medium_path: str):
        """Procedure to finalize a processed image."""
        self.state = ImageStatus.COMPLETED
        self.thumb_url = thumb_path
        self.medium_url = medium_path

    def mark_as_failed(self):
        """Procedure to mark a failed job."""
        self.state = ImageStatus.FAILED

    @classmethod
    def create_profile_img(cls, user_id: int, original_url: str):
        """ class method to create a profile photo object with at least input
        user_id: int - user identifier
        original_url: str - original image url
        Returns:
            ProfilePhoto: profile photo entity (with default values and PROCESSING status)
        """
    
        return cls(
            id=None,
            user_id=user_id,
            original_url=original_url,
            is_active=False,
            thumb_url=None,
            medium_url=None,
        )