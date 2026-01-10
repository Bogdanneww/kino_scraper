import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_movie_details_success(monkeypatch):
    async def mock_scrape_movie_details(title):
        return {
            "title": title,
            "year": 2023,
            "rating": 7.5,
            "genres": ["Action"],
            "description": "Test",
            "poster": "https://example.com/img.jpg",
            "url": "https://ua.kinorium.com/movie/1/",
        }

    async def mock_save_result(session, movie): return None

    monkeypatch.setattr("app.api.routers.scraping.scrape_movie_details", mock_scrape_movie_details)
    monkeypatch.setattr("app.api.routers.scraping.save_result", mock_save_result)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/scrape/movie/details", json={"title": "Inception"})

    assert response.status_code == 200
    assert response.json()["title"] == "Inception"
    assert "url" in response.json()
