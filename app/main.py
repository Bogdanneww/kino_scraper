from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routers import scraping
from app.schemas.common import StatusResponse
from app.db.database import engine
from app.db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables during application startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


def create_app() -> FastAPI:
    """Initialize and configure the FastAPI application."""
    app = FastAPI(
        title="Kino Scraper API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(scraping.router)

    @app.get("/", response_model=StatusResponse, tags=["Health"])
    async def root() -> StatusResponse:
        """Health check endpoint."""
        return {"status": "ok"}

    return app


app = create_app()
