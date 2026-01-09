from fastapi import FastAPI

from app.api.routers import scraping
from app.schemas.common import StatusResponse
from app.db.database import engine
from app.db.models import Base


def create_app() -> FastAPI:
    app = FastAPI(
        title="Kino Scraper API",
        version="0.1.0",
    )

    app.include_router(scraping.router)

    @app.on_event("startup")
    async def on_startup() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.get("/", response_model=StatusResponse, tags=["Health"])
    async def root() -> StatusResponse:
        return {"status": "ok"}

    return app


app = create_app()
