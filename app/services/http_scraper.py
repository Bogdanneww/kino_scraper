import httpx
from bs4 import BeautifulSoup
from app.core.config import settings

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
}


async def scrape_movies_by_genre(genre: str, page: int = 1) -> list[dict]:
    """Scrape movie list using HTTP requests and BeautifulSoup."""
    url = f"{settings.BASE_URL}/R2D2/?genres[]={genre}&page={page}&order=rating"

    async with httpx.AsyncClient(
        timeout=settings.HTTP_TIMEOUT, follow_redirects=True
    ) as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            return []

    soup = BeautifulSoup(response.text, "html.parser")
    movies = []

    for item in soup.select(".item .info .title a"):
        href = item.get("href")
        if href:
            movies.append(
                {
                    "title": item.get_text(strip=True),
                    "url": settings.BASE_URL + href if href.startswith("/") else href,
                }
            )

    return movies
