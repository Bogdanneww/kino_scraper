from httpx import AsyncClient
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_root_status():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
