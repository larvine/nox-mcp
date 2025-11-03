"""Common types used across the MCP server."""

from datetime import datetime
from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool
    data: T | None = None
    error: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    cursor: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Pagination response."""

    items: list[T]
    total: int
    page: int
    page_size: int
    has_more: bool
    next_cursor: str | None = None


class UserIdentity(BaseModel):
    """User identity information."""

    id: str
    email: str
    name: str | None = None
    employee_id: str | None = None
    department: str | None = None


class TimeRange(BaseModel):
    """Time range specification."""

    start: datetime  # ISO 8601 datetime
    end: datetime  # ISO 8601 datetime
    timezone: str | None = None


class AvailabilityStatus(str, Enum):
    """Resource availability status."""

    AVAILABLE = "available"
    BUSY = "busy"
    TENTATIVE = "tentative"
    OUT_OF_OFFICE = "out_of_office"
    UNKNOWN = "unknown"


class ErrorCode(str, Enum):
    """Common error codes."""

    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
