"""Types for mail namespace."""

from enum import Enum

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class EmailStatus(str, Enum):
    """Email status."""

    DRAFT = "draft"
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    BOUNCED = "bounced"


class EmailPriority(str, Enum):
    """Email priority."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class EmailAddress(BaseModel):
    """Email address with optional name."""

    email: EmailStr
    name: str | None = None


class EmailBody(BaseModel):
    """Email body content."""

    text: str | None = None
    html: str | None = None


class Attachment(BaseModel):
    """Email attachment."""

    filename: str
    content_type: str
    size: int = Field(..., ge=0)
    data: str | None = None  # base64 encoded
    url: str | None = None


class Email(BaseModel):
    """Email message representation."""

    id: str
    thread_id: str | None = None
    subject: str
    body: EmailBody
    from_: EmailAddress = Field(..., alias="from")
    to: list[EmailAddress]
    cc: list[EmailAddress] | None = None
    bcc: list[EmailAddress] | None = None
    reply_to: EmailAddress | None = None
    attachments: list[Attachment] | None = None
    headers: dict[str, str] | None = None
    sent_at: str | None = None
    received_at: str | None = None
    status: EmailStatus
    labels: list[str] | None = None
    metadata: dict[str, str] | None = None

    model_config = ConfigDict(
        populate_by_name=True,  # 예전 Config.populate_by_name=True 대체
        json_schema_extra={
            "title": "Email",
            "description": "Email message representation for MCP",
        },
    )


class EmailThread(BaseModel):
    """Email thread."""

    id: str
    subject: str
    participants: list[EmailAddress]
    messages: list[Email]
    message_count: int = Field(..., ge=0)
    last_message_at: str
    labels: list[str] | None = None


class SendEmailRequest(BaseModel):
    """Request to send an email."""

    to: str | list[str] = Field(..., min_length=1)
    cc: str | list[str] | None = None
    bcc: str | list[str] | None = None
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    html: str | None = None
    attachments: list[Attachment] | None = None
    reply_to: str | None = None
    in_reply_to: str | None = Field(None, description="Message ID for threading")
    priority: EmailPriority = EmailPriority.NORMAL


class CreateDraftRequest(BaseModel):
    """Request to create an email draft."""

    to: str | list[str] | None = None
    cc: str | list[str] | None = None
    bcc: str | list[str] | None = None
    subject: str | None = None
    body: str | None = None
    html: str | None = None
    attachments: list[Attachment] | None = None


class SearchEmailsRequest(BaseModel):
    """Request to search emails."""

    query: str | None = None
    from_: str | None = Field(None, alias="from")
    to: str | None = None
    subject: str | None = None
    date_range: dict[str, str] | None = None
    has_attachment: bool | None = None
    labels: list[str] | None = None
    limit: int = Field(default=20, ge=1, le=100)

    model_config = ConfigDict(
        populate_by_name=True,  # 예전 Config.populate_by_name=True 대체
        json_schema_extra={
            "title": "SearchEmailsRequest",
            "description": "Request to search emails for MCP",
        },
    )
