from domain.entities import ProfilePhoto, User
from infrastructure.db.repositories import SQLAlchemyUserRepository


class ToUserEntity:
    def __rmatmul__(self, model: "User") -> "User":
        return User(
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
