from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.common import StatusResponse
from app.schemas.scraping import GenreResponse
from app.schemas.movie import MovieShort, MovieDetails
from app.services.http_scraper import scrape_movies_by_genre
from app.services.search import find_movie_url
from app.services.browser_scraper import (
    scrape_movie_details,
    open_movie_in_browser,
)
from app.crud.scraping_result import save_result
from app.db.database import get_async_session


router = APIRouter(prefix="/scrape", tags=["Scraping"])


class MovieRequest(BaseModel):
    title: str


@router.get(
    "/genre",
    response_model=GenreResponse,
    summary="Scrape movies by genre",
    description="Fetches a list of movies from Kinorium by genre and page number",
    status_code=200,
)
async def scrape_by_genre(
    genre: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
):
    try:
        movies_data = await scrape_movies_by_genre(genre, page)
    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch data from Kinorium",
        )

    movies = [MovieShort(**movie) for movie in movies_data]

    return GenreResponse(
        genre=genre,
        page=page,
        count=len(movies),
        movies=movies,
    )


@router.post(
    "/movie/details",
    response_model=MovieDetails,
    summary="Get detailed movie information",
    description="Searches for a movie on Kinorium and scrapes detailed information",
    status_code=200,
)
async def get_movie_details(
    request: MovieRequest,
    session: AsyncSession = Depends(get_async_session),
):
    url = await find_movie_url(request.title)
    if not url:
        raise HTTPException(
            status_code=404,
            detail="Movie not found",
        )

    try:
        data = await scrape_movie_details(url)
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Browser scraping error",
        )

    movie = MovieDetails(**data)
    await save_result(session, movie)

    return movie


@router.post(
    "/movie/open",
    response_model=StatusResponse,
    summary="Open movie page in browser",
    description="Opens the movie page in a visible (non-headless) browser window",
    status_code=200,
)
async def open_movie(request: MovieRequest):
    url = await find_movie_url(request.title)
    if not url:
        raise HTTPException(
            status_code=404,
            detail="Movie not found",
        )

    await open_movie_in_browser(url)

    return {"status": "opened"}
