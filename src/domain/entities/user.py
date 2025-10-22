from dataclasses import dataclass
import datetime
from email.headerregistry import Address
from typing import List, Optional

from domain.entities.profile_photo import ProfilePhoto
from domain.entities.relationship import CustomerRelationship
from domain.value_objects.gender import Gender
from domain.value_objects.image_status import ImageStatus


@dataclass
class User:
    """ User entity """
    id: Optional[int]
    username: str
    first_name: str
    last_name: str
    gender: Gender
    customer_id: str
    birthday: datetime.date
    address: Optional[Address]
    photos: Optional[List[ProfilePhoto]]
    relationship: Optional[CustomerRelationship]
    created: Optional[datetime.datetime]
    last_updated: Optional[datetime.datetime]
    
    def add_new_photo(self, original_url: str) -> ProfilePhoto:
        """
        business process to activate user profile photo
        """
        self._deactivate_all_photos()

        new_photos = ProfilePhoto.create_profile_img(
            user_id=self.id,
            original_url=original_url
        )
        
        self.photos.append(new_photos)
        return new_photos

    def activate_photo(self, photo_id_to_activate: int):
        """
        activate photo after it processed completely
        rule: just one photo can be activate
        """
        found = False
        for photo in self.photos:
            if photo.id == photo_id_to_activate:
                if photo.status != ImageStatus.COMPLETED:
                    raise Exception(f"Cannot activate non-complete photo {photo.id}")
                photo.is_active = True
                found = True
            else:
                photo.is_active = False
        
        if not found:
            raise Exception(f"Photo {photo_id_to_activate} not found for user {self.id}")

    def find_photo_by_id(self, photo_id: int) -> Optional[ProfilePhoto]:
        return next((photo for photo in self.photos if photo.id == photo_id), None)

    def _deactivate_all_photos(self):
        """Internal helper to enforce the business rule."""
        for img in self.photos:
            img.is_active = False
