import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_genre_scraping_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/scrape/genre", params={"genre": "action"})
    assert response.status_code == 200
    data = response.json()
    assert "genre" in data
    assert data["genre"] == "action"
    assert "movies" in data
    assert isinstance(data["movies"], list)


@pytest.mark.asyncio
async def test_genre_scraping_invalid_genre():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/scrape/genre", params={"genre": "a"})
    assert response.status_code == 422
