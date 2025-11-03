"""MCP Server implementation."""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from corp_collab_mcp.config import get_settings
from corp_collab_mcp.namespaces import (
    directory,
    docs,
    mail,
    meetings,
    policies,
    rooms,
    tasks,
)
from corp_collab_mcp.namespaces import utils as ns_utils
from corp_collab_mcp.utils.logger import Logger

logger = Logger("server")

# Initialize server
app = Server("corp-collab-mcp")


# Tool definitions
TOOLS: list[Tool] = [
    # Meetings namespace
    Tool(
        name="meetings.create",
        description="Create a new calendar event/meeting",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "attendees": {"type": "array", "items": {"type": "string"}},
                "time_range": {
                    "type": "object",
                    "properties": {
                        "start": {"type": "string"},
                        "end": {"type": "string"},
                        "timezone": {"type": "string"},
                    },
                    "required": ["start", "end"],
                },
                "location": {"type": "string"},
                "recurrence": {"type": "object"},
            },
            "required": ["title", "attendees", "time_range"],
        },
    ),
    Tool(
        name="meetings.get",
        description="Get meeting details by ID",
        inputSchema={
            "type": "object",
            "properties": {"meeting_id": {"type": "string"}},
            "required": ["meeting_id"],
        },
    ),
    Tool(
        name="meetings.list",
        description="List meetings for a user within a time range",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "start": {"type": "string"},
                "end": {"type": "string"},
            },
            "required": ["user_id", "start", "end"],
        },
    ),
    Tool(
        name="meetings.findSlots",
        description="Find available time slots for meeting participants",
        inputSchema={
            "type": "object",
            "properties": {
                "attendees": {"type": "array", "items": {"type": "string"}},
                "duration": {"type": "integer"},
                "time_range": {"type": "object"},
                "preferred_times": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["attendees", "duration", "time_range"],
        },
    ),
    # Rooms namespace
    Tool(
        name="rooms.search",
        description="Search for available meeting rooms",
        inputSchema={
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "building": {"type": "string"},
                "floor": {"type": "string"},
                "min_capacity": {"type": "integer"},
                "features": {"type": "array", "items": {"type": "string"}},
                "time_range": {"type": "object"},
            },
            "required": ["time_range"],
        },
    ),
    Tool(
        name="rooms.reserve",
        description="Reserve a meeting room",
        inputSchema={
            "type": "object",
            "properties": {
                "room_id": {"type": "string"},
                "time_range": {"type": "object"},
                "purpose": {"type": "string"},
                "attendee_count": {"type": "integer"},
            },
            "required": ["room_id", "time_range"],
        },
    ),
    # Mail namespace
    Tool(
        name="mail.send",
        description="Send an email",
        inputSchema={
            "type": "object",
            "properties": {
                "to": {"type": ["string", "array"]},
                "cc": {"type": ["string", "array"]},
                "bcc": {"type": ["string", "array"]},
                "subject": {"type": "string"},
                "body": {"type": "string"},
                "html": {"type": "string"},
                "priority": {"type": "string"},
            },
            "required": ["to", "subject", "body"],
        },
    ),
    Tool(
        name="mail.createDraft",
        description="Create an email draft",
        inputSchema={
            "type": "object",
            "properties": {
                "to": {"type": ["string", "array"]},
                "subject": {"type": "string"},
                "body": {"type": "string"},
            },
        },
    ),
    # Directory namespace
    Tool(
        name="directory.searchUsers",
        description="Search for users in the directory",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "department": {"type": "string"},
                "title": {"type": "string"},
                "location": {"type": "string"},
            },
        },
    ),
    Tool(
        name="directory.resolveIdentities",
        description="Resolve multiple identifiers to canonical user/group IDs",
        inputSchema={
            "type": "object",
            "properties": {
                "identifiers": {"type": "array", "items": {"type": "string"}},
                "include_inactive": {"type": "boolean"},
            },
            "required": ["identifiers"],
        },
    ),
    # Tasks namespace
    Tool(
        name="tasks.create",
        description="Create a new task/issue",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "priority": {"type": "string"},
                "assignee_id": {"type": "string"},
            },
            "required": ["title"],
        },
    ),
    # Policies namespace
    Tool(
        name="policies.getWorkingHours",
        description="Get working hours for a timezone or user",
        inputSchema={
            "type": "object",
            "properties": {"timezone": {"type": "string"}, "user_id": {"type": "string"}},
        },
    ),
    Tool(
        name="policies.listHolidays",
        description="List holidays for a year/region",
        inputSchema={
            "type": "object",
            "properties": {
                "year": {"type": "integer"},
                "country": {"type": "string"},
                "region": {"type": "string"},
            },
            "required": ["year"],
        },
    ),
    # Utils namespace
    Tool(
        name="utils.convertTimezone",
        description="Convert datetime between timezones",
        inputSchema={
            "type": "object",
            "properties": {
                "dt": {"type": "string"},
                "from_tz": {"type": "string"},
                "to_tz": {"type": "string"},
            },
            "required": ["dt", "from_tz", "to_tz"],
        },
    ),
    Tool(
        name="utils.healthCheck",
        description="Check health status of all services",
        inputSchema={"type": "object", "properties": {}},
    ),
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Any:
    """Call a tool by name."""
    logger.info(f"Tool called: {name}", {"arguments": arguments})

    try:
        # Route to appropriate namespace handler
        if name.startswith("meetings."):
            handler_name = name.replace("meetings.", "")
            handler = getattr(meetings.handlers, handler_name.replace(".", "_"), None)
        elif name.startswith("rooms."):
            handler_name = name.replace("rooms.", "")
            handler = getattr(rooms.handlers, handler_name.replace(".", "_"), None)
        elif name.startswith("mail."):
            handler_name = name.replace("mail.", "")
            handler = getattr(mail.handlers, handler_name.replace(".", "_"), None)
        elif name.startswith("directory."):
            handler_name = name.replace("directory.", "")
            handler = getattr(directory.handlers, handler_name.replace(".", "_"), None)
        elif name.startswith("tasks."):
            handler_name = name.replace("tasks.", "")
            handler = getattr(tasks.handlers, handler_name.replace(".", "_"), None)
        elif name.startswith("docs."):
            handler_name = name.replace("docs.", "")
            handler = getattr(docs.handlers, handler_name.replace(".", "_"), None)
        elif name.startswith("policies."):
            handler_name = name.replace("policies.", "")
            handler = getattr(policies.handlers, handler_name.replace(".", "_"), None)
        elif name.startswith("utils."):
            handler_name = name.replace("utils.", "")
            handler = getattr(ns_utils.handlers, handler_name.replace(".", "_"), None)
        else:
            raise ValueError(f"Unknown tool: {name}")

        if handler is None:
            raise ValueError(f"Handler not found for tool: {name}")

        # Call the handler
        result = await handler(**arguments)
        return {"success": True, "data": result}

    except Exception as e:
        logger.error(f"Tool execution failed: {name}", {"error": str(e)})
        return {"success": False, "error": {"message": str(e)}}


async def main() -> None:
    """Main entry point."""
    settings = get_settings()
    logger.info("Starting Corp Collab MCP Server", {"version": "1.0.0"})

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
