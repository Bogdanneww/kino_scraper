from fastapi import FastAPI
from app.api.routers import scraping

app = FastAPI(
    title="Kinorium Scraper API",
    version="0.1.0",
)

app.include_router(scraping.router)

@app.get("/")
async def root():
    return {"status": "ok"}
