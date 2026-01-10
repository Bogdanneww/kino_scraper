from pydantic import BaseModel, HttpUrl, Field


class MovieShort(BaseModel):
    """Basic movie info for search results or lists."""
    title: str
    url: HttpUrl


class MovieDetails(BaseModel):
    """Comprehensive movie details for storage and display."""
    title: str
    year: int | None = None
    rating: float | None = None
    genres: list[str] = Field(default_factory=list)
    description: str | None = None
    poster: HttpUrl | None = None
    url: HttpUrl

    model_config = {"from_attributes": True}
