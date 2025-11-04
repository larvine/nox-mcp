"""Mail namespace - email sending, drafts, threads."""

from . import handlers
from .types import *

__all__ = [
    "handlers",
    "Email",
    "EmailBody",
    "EmailAddress",
    "EmailStatus",
    "Attachment",
    "EmailThread",
    "SendEmailRequest",
    "CreateDraftRequest",
    "SearchEmailsRequest",
    "EmailPriority",
]
