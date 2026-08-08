from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_MAIN_DATABASE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


def get_settings():
    return Settings()