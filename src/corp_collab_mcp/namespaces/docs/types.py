"""Types for docs namespace."""

from enum import Enum

from pydantic import BaseModel, Field, HttpUrl

from corp_collab_mcp.types.common import UserIdentity


class PermissionLevel(str, Enum):
    """Document permission level."""

    VIEW = "view"
    COMMENT = "comment"
    EDIT = "edit"
    ADMIN = "admin"


class DocumentPermission(BaseModel):
    """Document permission entry."""

    user: UserIdentity | None = None
    group_id: str | None = None
    level: PermissionLevel


class Document(BaseModel):
    """Document representation."""

    id: str
    title: str
    url: HttpUrl
    owner: UserIdentity
    created_at: str
    updated_at: str
    mime_type: str | None = None
    size: int | None = Field(None, ge=0)
    permissions: list[DocumentPermission] | None = None
    parent_id: str | None = None
    path: str | None = None
    metadata: dict[str, str] | None = None


class SearchDocsRequest(BaseModel):
    """Request to search documents."""

    query: str | None = None
    owner_id: str | None = None
    mime_type: str | None = None
    created_after: str | None = None
    created_before: str | None = None
    limit: int = Field(default=20, ge=1, le=100)


class ShareDocRequest(BaseModel):
    """Request to share a document."""

    document_id: str
    user_ids: list[str] | None = None
    group_ids: list[str] | None = None
    permission_level: PermissionLevel
    send_notification: bool = True
