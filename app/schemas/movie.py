from pydantic import BaseModel, HttpUrl


class MovieShort(BaseModel):
    title: str
    url: HttpUrl
