from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from app.core.config import settings


BASE = settings.BASE_URL.rstrip("/")


async def scrape_movies_by_genre(
    genre: int,
    page: int = 1,
    headless: bool = True,
) -> list[dict]:
    """
    Scraping movie list via JS-render (Playwright)
    """
    url = f"{BASE}/R2D2/?genres[]={genre}&page={page}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            locale="uk-UA",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page_obj = await context.new_page()

        await page_obj.goto(url, wait_until="networkidle")
        await page_obj.wait_for_selector(".filmList", timeout=20000)

        html = await page_obj.content()
        await browser.close()

    soup = BeautifulSoup(html, "html.parser")

    movies: list[dict] = []

    for item in soup.select(".filmList__item a[href]"):
        title = item.get_text(strip=True)
        href = item.get("href")

        if not title or not href:
            continue

        movies.append(
            {
                "title": title,
                "url": BASE + href,
            }
        )

    return movies


def _safe_int(value: str | None) -> int | None:
    if not value:
        return None
    digits = "".join(c for c in value if c.isdigit())
    return int(digits) if digits else None


def _safe_float(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return float(value.replace(",", ".").split()[0])
    except (ValueError, IndexError):
        return None


async def scrape_movie_details(
    title: str,
    headless: bool = True,
) -> dict:
    """
    Detailed movie page via search
    """
    search_url = f"{BASE}/search/?q={title}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(locale="uk-UA")
        page = await context.new_page()

        await page.goto(search_url, wait_until="networkidle")
        await page.wait_for_selector(".search-results-item a[href]", timeout=20000)

        first = page.locator(".search-results-item a[href]").first
        await first.click()

        await page.wait_for_selector("h1", timeout=20000)

        data = {
            "title": (await page.locator("h1").inner_text()).strip(),
            "year": _safe_int(
                await page.locator(".year").first.inner_text()
                if await page.locator(".year").count() > 0
                else None
            ),
            "rating": _safe_float(
                await page.locator(".ratingValue").first.inner_text()
                if await page.locator(".ratingValue").count() > 0
                else None
            ),
            "genres": await page.locator(".movie-page__genres a").all_text_contents(),
            "description": (
                await page.locator(".description").first.inner_text()
                if await page.locator(".description").count() > 0
                else None
            ),
            "poster": await page.get_attribute(".poster img", "src"),
            "url": page.url,
        }

        await browser.close()
        return data


async def open_movie_in_browser(title: str) -> None:
    search_url = f"{BASE}/search/?q={title}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(search_url)
        await page.wait_for_timeout(30000)
