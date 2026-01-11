import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_genre_scraping_success(monkeypatch):
    """Test successful movie scraping with mocked data."""

    async def mock_scrape_movies(genre, page):
        return [{"title": "Terminator", "url": "https://ua.kinorium.com/1/"}]

    monkeypatch.setattr(
        "app.api.routers.scraping.scrape_movies_by_genre", mock_scrape_movies
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/scrape/genre", params={"genre": 1, "page": 1})

    assert response.status_code == 200
    assert response.json()["count"] == 1


@pytest.mark.asyncio
async def test_genre_scraping_invalid_genre():
    """Verify validation error for invalid genre ID."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/scrape/genre", params={"genre": 0})
    assert response.status_code == 422
