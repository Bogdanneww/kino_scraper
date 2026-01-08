import httpx
from bs4 import BeautifulSoup
from app.core.config import settings


async def find_movie_url(title: str) -> str | None:
    search_url = f"{settings.BASE_URL}/search/"
    params = {"q": title}

    async with httpx.AsyncClient(
        timeout=settings.HTTP_TIMEOUT
    ) as client:
        response = await client.get(search_url, params=params)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    first_result = soup.select_one(
        ".search-results-item__title a[href]"
    )

    if not first_result:
        return None

    return settings.BASE_URL + first_result["href"]
