"""Configuration settings."""

import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    corp_api_base_url: str = Field(default="https://api.corp.internal", env="CORP_API_BASE_URL")
    corp_api_key: str = Field(default="", env="CORP_API_KEY")
    corp_api_timeout: int = Field(default=30, env="CORP_API_TIMEOUT")

    # Service-specific endpoints (optional)
    calendar_api_url: str | None = Field(default=None, env="CALENDAR_API_URL")
    mail_api_url: str | None = Field(default=None, env="MAIL_API_URL")
    directory_api_url: str | None = Field(default=None, env="DIRECTORY_API_URL")

    # Authentication
    auth_type: str = Field(default="api_key", env="AUTH_TYPE")
    oauth_client_id: str | None = Field(default=None, env="OAUTH_CLIENT_ID")
    oauth_client_secret: str | None = Field(default=None, env="OAUTH_CLIENT_SECRET")
    oauth_token_url: str | None = Field(default=None, env="OAUTH_TOKEN_URL")

    # Rate limiting
    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    max_requests_per_minute: int = Field(default=60, env="MAX_REQUESTS_PER_MINUTE")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    # Features
    enable_spam_filter: bool = Field(default=True, env="ENABLE_SPAM_FILTER")
    enable_rate_limiting: bool = Field(default=True, env="ENABLE_RATE_LIMITING")

    # WebSocket Server Configuration
    ws_host: str = Field(default="0.0.0.0", env="WS_HOST")
    ws_port: int = Field(default=8765, env="WS_PORT")
    transport: str = Field(default="ws", env="TRANSPORT")  # 'stdio' or 'ws'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
