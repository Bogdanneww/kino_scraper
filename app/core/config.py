from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = "https://ua.kinorium.com"
    HTTP_TIMEOUT: int = 10
    PLAYWRIGHT_HEADLESS: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
