# Standard
from pathlib import Path
from functools import lru_cache

# Backend
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


MAIN_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    # Database
    postgres_name: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = "database"
    postgres_port: int = 5432

    @computed_field
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_name}"
        )

    # LLM Engine
    ollama_host: str = "ollama"
    ollama_port: int = 11434

    @computed_field
    def ollama_url(self) -> str:
        return f"http://{self.ollama_host}:{self.ollama_port}"

    # Settings
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
