from playwright.async_api import async_playwright


async def scrape_movie_details(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, timeout=30000)

        data = {
            "title": await page.text_content("h1"),
            "year": await page.text_content(".film-page__year"),
            "rating": await page.text_content(".rating__value"),
            "genres": await page.locator(".film-genres a").all_text_contents(),
            "description": await page.text_content(".film-description"),
            "poster": await page.get_attribute(".film-poster img", "src"),
            "url": url,
        }

        await browser.close()

        return data


async def open_movie_in_browser(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
