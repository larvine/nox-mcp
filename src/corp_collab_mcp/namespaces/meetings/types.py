"""Types for meetings namespace."""

from enum import Enum

from pydantic import BaseModel, Field

from corp_collab_mcp.types.common import AvailabilityStatus, TimeRange, UserIdentity


class MeetingStatus(str, Enum):
    """Meeting status."""

    CONFIRMED = "confirmed"
    TENTATIVE = "tentative"
    CANCELLED = "cancelled"


class AttendeeStatus(str, Enum):
    """Attendee response status."""

    ACCEPTED = "accepted"
    DECLINED = "declined"
    TENTATIVE = "tentative"
    PENDING = "pending"


class RecurrencePattern(BaseModel):
    """Recurrence pattern for recurring meetings."""

    frequency: str = Field(..., pattern="^(daily|weekly|monthly|yearly)$")
    interval: int = Field(..., ge=1)
    end_date: str | None = None
    count: int | None = None


class MeetingAttendee(BaseModel):
    """Meeting attendee."""

    user: UserIdentity
    status: AttendeeStatus
    is_optional: bool = False


class Meeting(BaseModel):
    """Meeting/Event representation."""

    id: str
    title: str
    description: str | None = None
    organizer: UserIdentity
    attendees: list[MeetingAttendee]
    location: str | None = None
    time_range: TimeRange
    status: MeetingStatus
    recurrence: RecurrencePattern | None = None
    conference_link: str | None = None
    metadata: dict[str, str] | None = None


class TimeSlot(BaseModel):
    """Available time slot."""

    start: str
    end: str
    availability: AvailabilityStatus
    conflicts: list[Meeting] | None = None


class CreateMeetingRequest(BaseModel):
    """Request to create a new meeting."""

    title: str = Field(..., min_length=1)
    description: str | None = None
    attendees: list[str] = Field(..., min_length=1)  # User IDs or emails
    time_range: TimeRange
    location: str | None = None
    recurrence: RecurrencePattern | None = None


class FindSlotsRequest(BaseModel):
    """Request to find available time slots."""

    attendees: list[str] = Field(..., min_length=1)
    duration: int = Field(..., ge=1, description="Duration in minutes")
    time_range: TimeRange
    preferred_times: list[str] | None = Field(
        None, description="Preferred times, e.g., ['09:00', '14:00']"
    )
