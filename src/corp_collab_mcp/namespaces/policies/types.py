"""Types for policies namespace."""

from enum import Enum

from pydantic import BaseModel, Field


class DayOfWeek(str, Enum):
    """Day of week."""

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class WorkingHours(BaseModel):
    """Working hours configuration."""

    timezone: str
    days: dict[DayOfWeek, dict[str, str]]  # e.g., {"monday": {"start": "09:00", "end": "18:00"}}
    is_default: bool = False


class Holiday(BaseModel):
    """Holiday definition."""

    id: str
    name: str
    date: str
    is_recurring: bool = False
    applies_to: list[str] | None = None  # Countries, regions, or departments


class RateLimit(BaseModel):
    """Rate limit configuration."""

    resource: str  # e.g., "mail.send", "meetings.create"
    max_requests: int = Field(..., ge=1)
    window_seconds: int = Field(..., ge=1)
    per_user: bool = True


class SpamPolicy(BaseModel):
    """Spam/bulk sending policy."""

    max_recipients_per_email: int = Field(..., ge=1)
    max_emails_per_hour: int = Field(..., ge=1)
    max_emails_per_day: int = Field(..., ge=1)
    require_approval_threshold: int | None = None
    blocked_domains: list[str] | None = None


class PermissionPolicy(BaseModel):
    """Permission policy."""

    resource: str
    action: str
    allowed_roles: list[str]
    allowed_users: list[str] | None = None
    denied_users: list[str] | None = None
    conditions: dict[str, str] | None = None
