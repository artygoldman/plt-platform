from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str
    database_url_sync: str

    # Redis
    redis_url: str

    # Anthropic
    anthropic_api_key: str

    # S3/MinIO
    s3_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str

    # Security
    secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440

    # External API Integrations
    oura_client_id: Optional[str] = None
    oura_client_secret: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached singleton)."""
    return Settings()
