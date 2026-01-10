import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_genre_scraping_success(monkeypatch):
    async def mock_scrape_movies(genre, page):
        return [
            {"title": "Terminator", "url": "https://ua.kinorium.com/123/"},
            {"title": "Matrix", "url": "https://ua.kinorium.com/456/"}
        ]

    monkeypatch.setattr(
        "app.api.routers.scraping.scrape_movies_by_genre",
        mock_scrape_movies
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        response = await ac.get(
            "/scrape/genre",
            params={"genre": "action"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["genre"] == "action"
    assert data["count"] == 2
    assert data["movies"][0]["title"] == "Terminator"


@pytest.mark.asyncio
async def test_genre_scraping_invalid_genre():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        response = await ac.get(
            "/scrape/genre",
            params={"genre": "a"},
        )

    assert response.status_code == 422
