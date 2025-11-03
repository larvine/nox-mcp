"""Types for rooms namespace."""

from enum import Enum

from pydantic import BaseModel, Field

from corp_collab_mcp.types.common import TimeRange


class RoomFeature(str, Enum):
    """Meeting room features."""

    VIDEO_CONFERENCE = "video_conference"
    WHITEBOARD = "whiteboard"
    PROJECTOR = "projector"
    PHONE = "phone"
    ACCESSIBLE = "accessible"
    STANDING_DESK = "standing_desk"
    NATURAL_LIGHT = "natural_light"


class Equipment(BaseModel):
    """Room equipment."""

    type: str
    name: str
    quantity: int = Field(..., ge=1)


class MeetingRoom(BaseModel):
    """Meeting room representation."""

    id: str
    name: str
    location: str
    floor: str | None = None
    building: str | None = None
    capacity: int = Field(..., ge=1)
    features: list[RoomFeature] = []
    equipment: list[Equipment] = []
    is_active: bool = True
    metadata: dict[str, str] | None = None


class ReservationStatus(str, Enum):
    """Reservation status."""

    CONFIRMED = "confirmed"
    PENDING = "pending"
    CANCELLED = "cancelled"
    CHECKED_IN = "checked_in"
    NO_SHOW = "no_show"


class RoomReservation(BaseModel):
    """Room reservation."""

    id: str
    room: MeetingRoom
    reserved_by: str  # User ID
    time_range: TimeRange
    meeting_id: str | None = None
    purpose: str | None = None
    attendee_count: int | None = Field(None, ge=1)
    status: ReservationStatus


class RoomAvailability(BaseModel):
    """Room availability."""

    room: MeetingRoom
    available_slots: list[TimeRange]
    reservations: list[RoomReservation]


class SearchRoomsRequest(BaseModel):
    """Request to search for available meeting rooms."""

    location: str | None = None
    building: str | None = None
    floor: str | None = None
    min_capacity: int | None = Field(None, ge=1)
    features: list[RoomFeature] | None = None
    time_range: TimeRange


class ReserveRoomRequest(BaseModel):
    """Request to reserve a meeting room."""

    room_id: str
    time_range: TimeRange
    purpose: str | None = None
    attendee_count: int | None = Field(None, ge=1)
    meeting_id: str | None = None
