import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_open_movie_success(monkeypatch):
    async def mock_find_movie_url(title):
        return "https://ua.kinorium.com/fake-movie"

    async def mock_open_movie_in_browser(url):
        return None

    monkeypatch.setattr("app.services.search.find_movie_url", mock_find_movie_url)
    monkeypatch.setattr("app.services.browser_scraper.open_movie_in_browser", mock_open_movie_in_browser)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/scrape/movie/open", json={"title": "Fake Movie"})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "opened"
