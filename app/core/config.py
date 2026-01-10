from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str = "https://ua.kinorium.com"
    HTTP_TIMEOUT: int = 10
    PLAYWRIGHT_HEADLESS: bool = True
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
