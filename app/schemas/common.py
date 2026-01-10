from pydantic import BaseModel, HttpUrl


class StatusResponse(BaseModel):
    status: str


class OpenMovieResponse(StatusResponse):
    url: HttpUrl
