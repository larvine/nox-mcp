"""Custom error classes."""

from typing import Any

from corp_collab_mcp.types.common import ErrorCode


class McpError(Exception):
    """Base MCP error."""

    def __init__(self, code: ErrorCode, message: str, details: Any = None) -> None:
        """Initialize error."""
        super().__init__(message)
        self.code = code
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {
            "code": self.code.value,
            "message": str(self),
        }
        if self.details:
            result["details"] = self.details
        return result


class ValidationError(McpError):
    """Validation error."""

    def __init__(self, message: str, details: Any = None) -> None:
        """Initialize validation error."""
        super().__init__(ErrorCode.VALIDATION_ERROR, message, details)


class UnauthorizedError(McpError):
    """Unauthorized error."""

    def __init__(self, message: str = "Unauthorized") -> None:
        """Initialize unauthorized error."""
        super().__init__(ErrorCode.UNAUTHORIZED, message)


class NotFoundError(McpError):
    """Not found error."""

    def __init__(self, resource: str) -> None:
        """Initialize not found error."""
        super().__init__(ErrorCode.NOT_FOUND, f"{resource} not found")


class RateLimitError(McpError):
    """Rate limit error."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        """Initialize rate limit error."""
        super().__init__(ErrorCode.RATE_LIMIT_EXCEEDED, message)
