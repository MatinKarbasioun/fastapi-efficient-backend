import datetime
from typing import Optional
from sqlalchemy import (
    String, 
    BigInteger, 
    Boolean, 
    ForeignKey, 
    Index, 
    Enum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base
from .mixin import ExternalModelMixin

from domain.value_objects.image_status import ImageStatus


class ProfileImage(ExternalModelMixin, Base):
    __tablename__ = 'profile_image'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    
    original_url: Mapped[str] = mapped_column(String(512))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    
    thumb_url: Mapped[Optional[str]] = mapped_column(String(512))
    medium_url: Mapped[Optional[str]] = mapped_column(String(512))
    
    status: Mapped[ImageStatus] = mapped_column(
        Enum(ImageStatus), 
        default=ImageStatus.PROCESSING
    )

    user: Mapped["User"] = relationship(back_populates="photos")

    __table_args__ = (
        Index('ix_profile_image_user_active', 'user_id', 'is_active'),
    )