from fastapi import FastAPI

from app.api.routers import scraping
from app.schemas.common import StatusResponse


app = FastAPI(
    title="Kinorium Scraper API",
    version="0.1.0",
)

app.include_router(scraping.router)


@app.get("/", response_model=StatusResponse)
async def root():
    return {"status": "ok"}
