from typing import AsyncGenerator
from fastapi import Depends

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from settings import get_settings



settings = get_settings()


engine = create_async_engine(
    settings.database_url,
    echo=False
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
