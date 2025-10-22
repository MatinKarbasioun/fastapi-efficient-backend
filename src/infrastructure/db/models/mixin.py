import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func



class ExternalModelMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        index=True
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        index=True
    )