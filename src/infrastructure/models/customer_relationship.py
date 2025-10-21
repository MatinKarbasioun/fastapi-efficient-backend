import datetime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from sqlalchemy import (
    ForeignKey,
    BigInteger,
    TIMESTAMP,
    Index
)
from .mixin import ExternalModelMixin
from .base import Base



class CustomerRelationship(ExternalModelMixin, Base):
    __tablename__ = 'relationship'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user: Mapped["User"] = relationship(back_populates="relationship")
    points: Mapped[int] = mapped_column(BigInteger, default=0)
    last_activity: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    
    __table_args__ = (
        Index('ix_relationship_points_last_activity', 'points', 'last_activity'),
        Index('ix_relationship_user', 'user'),
        Index('ix_relationship_last_activity', 'last_activity')
    )


    def __str__(self):
        return f"{self.appuser.first_name} {self.appuser.last_name} with points: {self.points}"

    def __repr__(self):
        return (f"<CustomerRelationship(id={self.id!r}, user_id={self.user_id!r}, points={self.points!r})>")

