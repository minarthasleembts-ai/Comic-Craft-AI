from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    GEMINI_API_KEY: str = ""

    CLOUDFLARE_API_TOKEN: str = ""
    CLOUDFLARE_ACCOUNT_ID: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


def get_settings():
    return Settings()