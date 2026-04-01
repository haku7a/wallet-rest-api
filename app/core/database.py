from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
)


class Base(DeclarativeBase): ...


AsyncSessionLocal = async_sessionmaker(engine)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
