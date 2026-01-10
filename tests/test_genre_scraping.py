import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_genre_scraping_success(monkeypatch):
    async def mock_scrape_movies(genre, page):
        return [
            {"title": "Terminator", "url": "https://ua.kinorium.com/1/"},
            {"title": "Matrix", "url": "https://ua.kinorium.com/2/"}
        ]

    monkeypatch.setattr("app.api.routers.scraping.scrape_movies_by_genre", mock_scrape_movies)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/scrape/genre", params={"genre": 1, "page": 1})

    assert response.status_code == 200
    data = response.json()
    assert data["genre"] == 1
    assert data["count"] == 2
    assert data["movies"][0]["title"] == "Terminator"


@pytest.mark.asyncio
async def test_genre_scraping_invalid_genre():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/scrape/genre", params={"genre": 0})
    assert response.status_code == 422
