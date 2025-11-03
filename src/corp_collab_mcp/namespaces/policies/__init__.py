"""Policies namespace - working hours, holidays, permissions, spam/bulk sending limits."""

from . import handlers
from .types import *

__all__ = [
    "handlers",
    "WorkingHours",
    "Holiday",
    "RateLimit",
    "SpamPolicy",
    "PermissionPolicy",
]
