from pydantic import BaseModel, HttpUrl


class StatusResponse(BaseModel):
    """Standard API status response."""
    status: str


class OpenMovieResponse(StatusResponse):
    """Response containing the opened movie URL."""
    url: HttpUrl
