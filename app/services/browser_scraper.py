from playwright.async_api import async_playwright, Error as PlaywrightError
from app.core.config import settings


def _safe_int(value: str | None) -> int | None:
    if not value:
        return None
    digits = "".join(c for c in value if c.isdigit())
    return int(digits) if digits else None


def _safe_float(value: str | None) -> float | None:
    if not value:
        return None
    value = value.replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return None


async def scrape_movie_details(url: str) -> dict:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=settings.PLAYWRIGHT_HEADLESS
            )
            page = await browser.new_page()
            await page.goto(url, timeout=30_000)

            data = {
                "title": (await page.text_content("h1")) or "",
                "year": _safe_int(
                    await page.text_content(".film-page__year")
                ),
                "rating": _safe_float(
                    await page.text_content(".rating__value")
                ),
                "genres": await page.locator(
                    ".film-genres a"
                ).all_text_contents(),
                "description": await page.text_content(
                    ".film-description"
                ),
                "poster": await page.get_attribute(
                    ".film-poster img",
                    "src",
                ),
                "url": url,
            }

            await browser.close()
            return data

    except PlaywrightError as exc:
        raise RuntimeError("Browser scraping failed") from exc


async def open_movie_in_browser(url: str) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
