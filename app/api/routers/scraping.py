from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.movie import MovieDetails, MovieRequest
from app.schemas.scraping import GenreResponse
from app.services.browser_scraper import scrape_movie_details, open_movie_in_browser
from app.services.http_scraper import scrape_movies_by_genre
from app.db.database import get_async_session
from app.services.db_service import save_result

router = APIRouter(prefix="/scrape", tags=["Scraping"])


@router.get("/genre", response_model=GenreResponse)
async def scrape_genre(genre: int = Query(..., ge=1), page: int = Query(1, ge=1)):
    """Fetch movie list by genre and page using HTTP scraping."""
    movies = await scrape_movies_by_genre(genre=genre, page=page)
    return {"genre": genre, "page": page, "count": len(movies), "movies": movies}


@router.post("/movie/details", response_model=MovieDetails)
async def movie_details(
    request: MovieRequest, db: AsyncSession = Depends(get_async_session)
):
    """Scrape full movie details and save to the database."""
    try:
        data = await scrape_movie_details(request.title)
        details = MovieDetails(**data)
        await save_result(db, details)
        return details
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Scraping failed: {str(e)}")


@router.post("/movie/open")
async def open_movie(request: MovieRequest):
    """Search and open the movie page in a visible browser."""
    await open_movie_in_browser(request.title)
    return {"status": "opened"}
