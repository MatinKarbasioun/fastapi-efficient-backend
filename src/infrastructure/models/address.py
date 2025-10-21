from typing import Optional

from sqlalchemy import (
    Index,
    String,
    BigInteger,
    relationship
)
from sqlalchemy.orm import mapped_column, Mapped

from .mixin import ExternalModelMixin
from .base import Base


class Address(ExternalModelMixin, Base):
    __tablename__ = 'address'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    street: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    street_number: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    city_code: Mapped[str] = mapped_column(String(256))
    city: Mapped[str] = mapped_column(String(256), index=True)
    country: Mapped[str] = mapped_column(String(128), index=True)
    
    users: Mapped[list["User"]] = relationship(back_populates="address")


    __table_args__ = (
        Index('ix_address_street', 'street'),
        Index('ix_address_city_country', 'city', 'country'),
        Index('ix_address_street_street_number', 'street', 'street_number'),
        Index('ix_address_street_city', 'street', 'city')
    )

    def __str__(self):
        return f"{self.street}, {self.street_number}, {self.city_code}, {self.city}, {self.country}"

    def __repr__(self):
        return (f"<AddressModel(id={self.id!r}, street={self.street!r}, "
                f"city={self.city!r}, country={self.country!r})>")