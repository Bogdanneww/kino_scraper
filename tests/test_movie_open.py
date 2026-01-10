import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_open_movie_success(monkeypatch):
    async def mock_find_movie_url(title):
        return "https://ua.kinorium.com/fake-movie"

    async def mock_open_movie_in_browser(url):
        return None

    monkeypatch.setattr(
        "app.api.routers.scraping.find_movie_url",
        mock_find_movie_url,
    )
    monkeypatch.setattr(
        "app.api.routers.scraping.open_movie_in_browser",
        mock_open_movie_in_browser,
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        response = await ac.post(
            "/scrape/movie/open",
            json={"title": "Fake Movie"},
        )

    assert response.status_code == 200
    assert response.json() == {"status": "opened"}
