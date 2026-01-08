import httpx
from bs4 import BeautifulSoup
from app.core.config import settings


async def scrape_movies_by_genre(
    genre: str,
    page: int = 1,
) -> list[dict]:
    url = f"{settings.BASE_URL}/films/{genre}/?page={page}"

    async with httpx.AsyncClient(
        timeout=settings.HTTP_TIMEOUT
    ) as client:
        response = await client.get(url)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    movies: list[dict] = []

    for item in soup.select(".filmListItem"):
        title = item.select_one(".filmListItem__title")
        if not title or not title.get("href"):
            continue

        movies.append(
            {
                "title": title.text.strip(),
                "url": settings.BASE_URL + title["href"],
            }
        )

    return movies
