"""Meetings namespace - calendar events, time slots, availability."""

from . import handlers
from .types import *

__all__ = [
    "handlers",
    "Meeting",
    "MeetingAttendee",
    "MeetingStatus",
    "AttendeeStatus",
    "RecurrencePattern",
    "TimeSlot",
    "CreateMeetingRequest",
    "FindSlotsRequest",
]
