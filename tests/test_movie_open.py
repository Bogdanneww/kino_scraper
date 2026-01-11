import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_open_movie_success(monkeypatch):
    """Test the endpoint for opening a movie page in a visible browser."""

    async def mock_open_browser(title):
        return None

    monkeypatch.setattr(
        "app.api.routers.scraping.open_movie_in_browser", mock_open_browser
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/scrape/movie/open", json={"title": "Interstellar"})

    assert response.status_code == 200
    assert response.json() == {"status": "opened"}
