from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    app_name: str = "Photo Processing App"
    version: str = "0.0.1"
    actor_name: str = "thumbnail_processor_actor"

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")
    

@lru_cache
def get_settings() -> Settings:
    """Returns the cached settings instance."""
    return Settings()
