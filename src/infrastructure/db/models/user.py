import datetime
from typing import List, Optional

from sqlalchemy import String, BigInteger, Date, ForeignKey, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TSVECTOR

from .base import Base
from .mixin import ExternalModelMixin
from .address import Address as AddressModel
from .customer_relationship import CustomerRelationship as Relationship
from .profile_photo import ProfileImage


class User(ExternalModelMixin, Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128), index=True)
    gender: Mapped[str] = mapped_column(String(12))
    customer_id: Mapped[str] = mapped_column(String(64), unique=True)
    relationship_id: Mapped[int] = mapped_column(ForeignKey("relationship.id", ondelete="CASCADE"), unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(32), nullable=True, index=True)
    birthday: Mapped[datetime.datetime] = mapped_column(Date, nullable=True, index=True)
    address_id: Mapped[Optional[int]] = mapped_column(ForeignKey("address.id", ondelete="CASCADE"), nullable=True)
    search_vector: Mapped[Optional[str]] = mapped_column(TSVECTOR, nullable=True)
    
    
    address: Mapped["AddressModel"] = relationship(back_populates="users")
    relationship: Mapped["Relationship"] = relationship(back_populates="user")
    photos: Mapped[List["ProfileImage"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin" 
    )
    
    images: Mapped[List["ProfileImageModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    
    __table_args__ = (
        Index('ix_user_first_name_last_name', 'first_name', 'last_name'),
        Index('ix_created_gender', 'created_at', 'gender'),
        Index('ix_search_vector', 'search_vector', postgresql_using='gin')
    )
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} with customer id: {self.customer_id}'

    def __repr__(self):
        # A more idiomatic SQLAlchemy __repr__
        return (f"<UserModel(id={self.id!r}, "
                f"first_name={self.first_name!r}, "
                f"last_name={self.last_name!r}, "
                f"gender={self.gender!r}, "
                f"customer_id={self.customer_id!r})>")