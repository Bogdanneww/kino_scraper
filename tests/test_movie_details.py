import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_movie_details_success(monkeypatch):
    async def mock_find_movie_url(title):
        return "https://ua.kinorium.com/fake-movie"

    async def mock_scrape_movie_details(url):
        return {
            "title": "Fake Movie",
            "year": 2023,
            "rating": 7.5,
            "genres": ["Action", "Drama"],
            "description": "Fake description",
            "poster": "https://example.com/poster.jpg",
            "url": url,
        }

    async def mock_save_result(session, movie):
        return None

    monkeypatch.setattr(
        "app.api.routers.scraping.find_movie_url",
        mock_find_movie_url,
    )
    monkeypatch.setattr(
        "app.api.routers.scraping.scrape_movie_details",
        mock_scrape_movie_details,
    )
    monkeypatch.setattr(
        "app.api.routers.scraping.save_result",
        mock_save_result,
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        response = await ac.post(
            "/scrape/movie/details",
            json={"title": "Fake Movie"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Fake Movie"
    assert data["url"] == "https://ua.kinorium.com/fake-movie"
    assert isinstance(data["genres"], list)
