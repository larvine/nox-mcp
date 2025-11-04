"""Types for utils namespace."""

from enum import Enum

from pydantic import BaseModel


class TimezoneInfo(BaseModel):
    """Timezone information."""

    name: str
    offset: str
    abbreviation: str
    is_dst: bool


class ICSEvent(BaseModel):
    """ICS calendar event."""

    summary: str
    description: str | None = None
    location: str | None = None
    start: str
    end: str
    timezone: str | None = None
    organizer: str | None = None
    attendees: list[str] | None = None
    rrule: str | None = None  # Recurrence rule


class HealthStatus(str, Enum):
    """Service health status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheck(BaseModel):
    """Health check result."""

    status: HealthStatus
    timestamp: str
    services: dict[str, HealthStatus]
    details: dict[str, str] | None = None
