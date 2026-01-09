from fastapi import APIRouter, Query, HTTPException, status, Depends
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


router = APIRouter(
    prefix="/scrape",
    tags=["Scraping"],
)


class MovieRequest(BaseModel):
    """Request schema for movie-based actions."""
    title: str


@router.get(
    "/genre",
    response_model=GenreResponse,
    status_code=status.HTTP_200_OK,
    summary="Scrape movies by genre",
    description="Scrape a list of movies from Kinorium by genre using simple HTTP requests.",
)
async def scrape_by_genre(
    genre: str = Query(..., min_length=2, description="Movie genre"),
    page: int = Query(1, ge=1, description="Page number"),
):
    try:
        movies_data = await scrape_movies_by_genre(genre, page)
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
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
    status_code=status.HTTP_200_OK,
    summary="Get movie details",
    description="Scrape detailed movie information using a headless browser and save it to database.",
)
async def get_movie_details(
    request: MovieRequest,
    session: AsyncSession = Depends(get_async_session),
):
    url = await find_movie_url(request.title)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    data = await scrape_movie_details(url)

    movie = MovieDetails(**data)

    await save_result(session, movie)

    return movie


@router.post(
    "/movie/open",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Open movie page in browser",
    description="Open movie page in a non-headless browser.",
)
async def open_movie(request: MovieRequest):
    url = await find_movie_url(request.title)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    await open_movie_in_browser(url)

    return {"status": "opened"}
