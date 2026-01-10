from playwright.async_api import async_playwright
from app.core.config import settings
from app.services.http_scraper import HEADERS


async def find_movie_url(title: str) -> str | None:
    """Search for a movie and return its direct URL."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.PLAYWRIGHT_HEADLESS)
        context = await browser.new_context(user_agent=HEADERS["User-Agent"])
        page = await context.new_page()

        try:
            await page.goto(
                f"{settings.BASE_URL}/search/?q={title}",
                wait_until="networkidle",
                timeout=15000,
            )

            movie_link_selector = (
                ".item.search[data-type='movie'] .title a, .item.search .title a"
            )
            await page.wait_for_selector(movie_link_selector, timeout=10000)

            link_element = page.locator(movie_link_selector).first
            href = await link_element.get_attribute("href")

            if not href:
                return None

            full_url = settings.BASE_URL + href if href.startswith("/") else href
            return full_url

        except Exception:
            return None
        finally:
            await browser.close()
