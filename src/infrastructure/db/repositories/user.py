from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from domain.entities.user import User as UserEntity
from domain.entities import ProfilePhoto
from domain.repositories.persistence.user import IUserRepository
from infrastructure.db.models.user import User as UserModel
from infrastructure.db.models.profile_photo import ProfilePhoto as ProfilePhotoModel



class SQLAlchemyUserRepository(IUserRepository):
    """SQLAlchemy implementation of the User Repository."""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        stmt = select(UserModel).options(selectinload(UserModel.images)).where(UserModel.id == user_id)
        model = await self.session.scalar(stmt)
        return self._to_entity(model) if model else None

    async def save(self, user: UserEntity) -> UserEntity:
        """Saves the User aggregate, handling adds/updates of children."""
        if user.id is None:
             # Create new user model
             model = UserModel(username=user.username)
             self.session.add(model)
             await self.session.flush()
             user.id = model.id # Update entity ID
             print(f"Created new user with ID: {user.id}")
        else:
            model = await self.session.get(UserModel, user.id, options=[selectinload(UserModel.images)])
            if not model:
                raise ValueError(f"User {user.id} not found for update.")
            model.username = user.username # Update scalar fields

        # Sync images (simplified - assumes new images have no ID)
        db_image_map = {img.id: img for img in model.images if img.id is not None}
        new_db_images = []

        for entity_image in user.images:
            if entity_image.id is None: # New image to add
                db_image = ProfilePhotoModel(
                    user_id=model.id,
                    original_url=entity_image.original_url,
                    is_active=entity_image.is_active,
                    status=entity_image.status,
                    thumb_url=entity_image.thumb_url,
                    medium_url=entity_image.medium_url,
                    created_at=entity_image.created_at
                )
                self.session.add(db_image)
                new_db_images.append((entity_image, db_image)) # Keep track to update ID later
            elif entity_image.id in db_image_map: # Existing image to update
                 db_image = db_image_map[entity_image.id]
                 db_image.is_active = entity_image.is_active
                 db_image.status = entity_image.status
                 db_image.original_url = entity_image.original_url
                 db_image.thumb_url = entity_image.thumb_url
                 db_image.medium_url = entity_image.medium_url
            # Deletion logic would go here if needed

        await self.session.flush() # Flush to get IDs for newly added images

        # Update entity IDs for newly added images
        for entity_image, db_image in new_db_images:
            entity_image.id = db_image.id
            print(f"Assigned ID {db_image.id} to new image for user {user.id}")


        return user # Return the updated entity

    def _to_entity(self, model: UserModel) -> UserEntity:
        """Maps DB model to Domain entity."""
        return UserEntity(
            id=model.id,
            username=model.username,
            images=[
                ProfilePhoto(
                    id=img.id,
                    user_id=img.user_id,
                    original_url=img.original_url,
                    is_active=img.is_active,
                    status=img.status,
                    thumb_url=img.thumb_url,
                    medium_url=img.medium_url,
                    created_at=img.created_at
                ) for img in model.images
            ]
        )