"""Configuration settings for the application."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/contract_db"

    # Application
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    # NLP Model
    nlp_model_name: str = "dslim/bert-base-NER"
    max_upload_size: int = 10485760  # 10MB

    # CORS - use string to avoid JSON parsing issues
    cors_origins_str: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        validation_alias="CORS_ORIGINS",
    )

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins_str.split(",")]

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
