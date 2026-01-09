from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Movie
from app.schemas.movie import MovieDetails


async def save_result(
    session: AsyncSession,
    movie: MovieDetails,
) -> Movie:
    """
    Save scraped movie details to database.
    """

    db_movie = Movie(
        title=movie.title,
        year=movie.year,
        rating=movie.rating,
        genres=",".join(movie.genres),
        description=movie.description,
        poster=str(movie.poster) if movie.poster else None,
        url=str(movie.url),
    )

    session.add(db_movie)
    await session.commit()
    await session.refresh(db_movie)

    return db_movie
