from fastapi import APIRouter, Query, HTTPException
from app.services.http_scraper import scrape_movies_by_genre
from app.schemas.scraping import GenreResponse, MovieShort
import httpx

router = APIRouter(prefix="/scrape", tags=["Scraping"])

@router.get("/genre", response_model=GenreResponse)
async def scrape_by_genre(
    genre: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
):
    try:
        movies_data = await scrape_movies_by_genre(genre, page)
    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch data from Kinorium"
        )

    movies = [MovieShort(**movie) for movie in movies_data]

    return GenreResponse(
        genre=genre,
        page=page,
        count=len(movies),
        movies=movies
    )
