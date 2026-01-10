from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"

engine = create_async_engine(DATABASE_URL, echo=False)

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
