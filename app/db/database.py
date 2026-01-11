from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models."""

    pass


async def get_async_session() -> AsyncSession:
    """Dependency to provide an asynchronous database session."""
    async with AsyncSessionLocal() as session:
        yield session
