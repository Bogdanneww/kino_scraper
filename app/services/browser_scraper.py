from playwright.async_api import async_playwright
from app.core.config import settings
from app.services.http_scraper import HEADERS


def _safe_int(value: str | None) -> int | None:
    """Safely extract integer from string."""
    if not value:
        return None
    digits = "".join(c for c in value if c.isdigit())
    return int(digits) if digits else None


def _safe_float(value: str | None) -> float | None:
    """Safely extract float from string."""
    if not value:
        return None
    try:
        return float(value.replace(",", ".").split()[0])
    except:
        return None


async def scrape_movies_by_genre(genre: str, page_num: int = 1) -> list[dict]:
    """Scrape movie list by genre using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.PLAYWRIGHT_HEADLESS)
        page = await browser.new_page()
        url = f"{settings.BASE_URL}/R2D2/?genres[]={genre}&page={page_num}&order=rating"

        await page.goto(url, wait_until="networkidle", timeout=15000)
        await page.wait_for_selector(".item .info .title a", timeout=10000)

        movies = []
        links = page.locator(".item .info .title a")
        for i in range(min(await links.count(), 20)):
            el = links.nth(i)
            movies.append(
                {
                    "title": (await el.inner_text()).strip(),
                    "url": settings.BASE_URL + (await el.get_attribute("href")),
                }
            )
        await browser.close()
        return movies


async def scrape_movie_details(query: str) -> dict:
    """Scrape detailed movie data via search and headless browser."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.PLAYWRIGHT_HEADLESS)
        context = await browser.new_context(user_agent=HEADERS["User-Agent"])
        page = await context.new_page()
        try:
            await page.goto(
                f"{settings.BASE_URL}/search/?q={query}", wait_until="networkidle"
            )
            await page.locator(".item.search .title a").first.click()
            await page.wait_for_load_state("networkidle")

            return {
                "title": await page.get_attribute(
                    'meta[property="og:title"]', "content"
                ),
                "year": _safe_int(
                    await page.locator(
                        ".film-page__title-section .year"
                    ).first.inner_text()
                    if await page.locator(".film-page__title-section .year").count()
                    else None
                ),
                "rating": _safe_float(
                    await page.get_attribute('meta[itemprop="ratingValue"]', "content")
                    if await page.locator('meta[itemprop="ratingValue"]').count()
                    else None
                ),
                "genres": await page.locator(".film-page__genre a").all_text_contents(),
                "description": await page.get_attribute(
                    'meta[property="og:description"]', "content"
                ),
                "poster": await page.get_attribute(
                    'meta[property="og:image"]', "content"
                ),
                "url": page.url,
            }
        finally:
            await browser.close()


async def open_movie_in_browser(url: str) -> None:
    """Launch a visible browser window with the movie page."""
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto(url)
