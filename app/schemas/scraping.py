from pydantic import BaseModel
from .movie import MovieShort


class GenreResponse(BaseModel):
    genre: int
    page: int
    count: int
    movies: list[MovieShort]
