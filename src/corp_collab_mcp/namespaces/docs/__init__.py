"""Docs namespace (optional) - document links, permission verification."""

from . import handlers
from .types import *

__all__ = [
    "handlers",
    "Document",
    "DocumentPermission",
    "PermissionLevel",
    "SearchDocsRequest",
    "ShareDocRequest",
]
