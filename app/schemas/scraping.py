from pydantic import BaseModel
from .movie import MovieShort


class GenreResponse(BaseModel):
    genre: str
    page: int
    count: int
    movies: list[MovieShort]
