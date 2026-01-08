from fastapi import APIRouter, Query, HTTPException
from app.services.http_scraper import scrape_movies_by_genre
from app.services.search import find_movie_url
from app.services.browser_scraper import scrape_movie_details, open_movie_in_browser
from app.schemas.scraping import GenreResponse
from app.schemas.movie import MovieShort
import httpx
from pydantic import BaseModel

router = APIRouter(prefix="/scrape", tags=["Scraping"])


@router.get("/genre", response_model=GenreResponse)
async def scrape_by_genre(
    genre: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
):
    try:
        movies_data = await scrape_movies_by_genre(genre, page)
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Failed to fetch data from Kinorium")

    movies = [MovieShort(**movie) for movie in movies_data]

    return GenreResponse(
        genre=genre,
        page=page,
        count=len(movies),
        movies=movies
    )


class MovieRequest(BaseModel):
    title: str

@router.post("/movie/details")
async def get_movie_details(request: MovieRequest):
    url = await find_movie_url(request.title)
    if not url:
        raise HTTPException(status_code=404, detail="Movie not found")

    data = await scrape_movie_details(url)
    return data


@router.post("/movie/open")
async def open_movie(title: str):
    url = await find_movie_url(title)
    if not url:
        raise HTTPException(404, "Movie not found")

    await open_movie_in_browser(url)
    return {"status": "opened", "url": url}
