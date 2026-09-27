from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    GEMINI_API_KEY: str = ""
    HF_API_KEY: str = ""
    POLLINATIONS_API_KEY: str = ""
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


def get_settings():
    return Settings()