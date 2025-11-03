"""Rooms namespace - meeting rooms, availability, reservations."""

from . import handlers
from .types import *

__all__ = [
    "handlers",
    "MeetingRoom",
    "RoomFeature",
    "Equipment",
    "RoomReservation",
    "ReservationStatus",
    "RoomAvailability",
    "SearchRoomsRequest",
    "ReserveRoomRequest",
]
