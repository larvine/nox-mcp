"""Configuration settings."""

import os
from functools import lru_cache

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        json_schema_extra={
            "title": "Corp MCP Settings",
            "description": "사내 MCP 서버용 환경 설정",
        },
    )
    # Core
    corp_api_base_url: str = Field(
        default="https://api.corp.internal",
        validation_alias="CORP_API_BASE_URL",
        json_schema_extra={"example": "https://api.mycorp.com"},
        description="사내 API 베이스 URL",
    )
    corp_api_key: str = Field(
        default="",
        validation_alias="CORP_API_KEY",
        json_schema_extra={"secret": True, "example": "sk_live_xxx"},
        description="사내 API 키",
    )
    corp_api_timeout: int = Field(
        default=30,
        validation_alias="CORP_API_TIMEOUT",
        json_schema_extra={"unit": "seconds", "example": 30},
        description="API 호출 타임아웃(초)",
    )

    # Service-specific endpoints (optional)
    calendar_api_url: Optional[str] = Field(
        default=None,
        validation_alias="CALENDAR_API_URL",
        json_schema_extra={"nullable": True, "example": "https://calendar.corp/api"},
        description="캘린더 서비스 엔드포인트",
    )
    mail_api_url: Optional[str] = Field(
        default=None,
        validation_alias="MAIL_API_URL",
        json_schema_extra={"nullable": True, "example": "https://mail.corp/api"},
        description="메일 서비스 엔드포인트",
    )
    directory_api_url: Optional[str] = Field(
        default=None,
        validation_alias="DIRECTORY_API_URL",
        json_schema_extra={"nullable": True, "example": "https://directory.corp/api"},
        description="디렉터리 서비스 엔드포인트",
    )

    # Authentication
    auth_type: str = Field(
        default="api_key",
        validation_alias="AUTH_TYPE",
        json_schema_extra={"enum": ["api_key", "oauth2"], "example": "api_key"},
        description="인증 방식",
    )
    oauth_client_id: Optional[str] = Field(
        default=None,
        validation_alias="OAUTH_CLIENT_ID",
        json_schema_extra={"nullable": True},
        description="OAuth 클라이언트 ID",
    )
    oauth_client_secret: Optional[str] = Field(
        default=None,
        validation_alias="OAUTH_CLIENT_SECRET",
        json_schema_extra={"nullable": True, "secret": True},
        description="OAuth 클라이언트 시크릿",
    )
    oauth_token_url: Optional[str] = Field(
        default=None,
        validation_alias="OAUTH_TOKEN_URL",
        json_schema_extra={"nullable": True},
        description="OAuth 토큰 URL",
    )

    # Rate limiting
    rate_limit_enabled: bool = Field(
        default=True,
        validation_alias="RATE_LIMIT_ENABLED",
        json_schema_extra={"example": True},
        description="레이트리밋 사용 여부",
    )
    max_requests_per_minute: int = Field(
        default=60,
        validation_alias="MAX_REQUESTS_PER_MINUTE",
        json_schema_extra={"example": 60, "unit": "rpm"},
        description="분당 최대 요청 수",
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        validation_alias="LOG_LEVEL",
        json_schema_extra={"enum": ["DEBUG", "INFO", "WARNING", "ERROR"]},
        description="로그 레벨",
    )
    log_format: str = Field(
        default="json",
        validation_alias="LOG_FORMAT",
        json_schema_extra={"enum": ["json", "text"]},
        description="로그 포맷",
    )

    # Features
    enable_spam_filter: bool = Field(
        default=True,
        validation_alias="ENABLE_SPAM_FILTER",
        json_schema_extra={"example": True},
        description="스팸 필터 사용",
    )
    enable_rate_limiting: bool = Field(
        default=True,
        validation_alias="ENABLE_RATE_LIMITING",
        json_schema_extra={"example": True},
        description="레이트리밋 기능 사용",
    )

    # WebSocket Server Configuration
    ws_host: str = Field(
        default="0.0.0.0",
        validation_alias="WS_HOST",
        json_schema_extra={"example": "0.0.0.0"},
        description="WebSocket 서버 호스트",
    )
    ws_port: int = Field(
        default=8765,
        validation_alias="WS_PORT",
        json_schema_extra={"example": 8765, "unit": "port"},
        description="WebSocket 서버 포트",
    )
    transport: str = Field(
        default="ws",
        validation_alias="TRANSPORT",
        json_schema_extra={"enum": ["stdio", "ws"], "example": "ws"},
        description="통신 방식 (stdio 또는 ws)",
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
