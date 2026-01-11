from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ScrapingResult
from app.schemas.movie import MovieDetails


async def save_result(
    session: AsyncSession,
    movie: MovieDetails,
) -> None:
    """Save movie details to the database asynchronously."""
    obj = ScrapingResult(
        title=movie.title,
        year=movie.year,
        rating=movie.rating,
        genres=", ".join(movie.genres),
        description=movie.description,
        poster=movie.poster,
        url=movie.url,
    )

    session.add(obj)
    await session.commit()
