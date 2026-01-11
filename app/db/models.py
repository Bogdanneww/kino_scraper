from sqlalchemy import String, Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ScrapingResult(Base):
    __tablename__ = "scraping_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    genres: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    poster: Mapped[str | None] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(500))
