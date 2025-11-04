"""MCP Server implementation using FastMCP."""

import asyncio

from fastmcp import FastMCP

from corp_collab_mcp.config import get_settings
from corp_collab_mcp.utils.logger import Logger

logger = Logger("server")

# Initialize FastMCP server
mcp = FastMCP("corp-collab-mcp")


# Import and register namespace tools
def register_namespaces() -> None:
    """Register all namespace tools."""
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

    # Register meetings tools
    mcp.tool()(meetings.handlers.create_meeting)
    mcp.tool()(meetings.handlers.get_meeting)
    mcp.tool()(meetings.handlers.update_meeting)
    mcp.tool()(meetings.handlers.cancel_meeting)
    mcp.tool()(meetings.handlers.list_meetings)
    mcp.tool()(meetings.handlers.find_available_slots)
    mcp.tool()(meetings.handlers.get_availability)

    # Register rooms tools
    mcp.tool()(rooms.handlers.search_rooms)
    mcp.tool()(rooms.handlers.get_room)
    mcp.tool()(rooms.handlers.get_room_availability)
    mcp.tool()(rooms.handlers.reserve_room)
    mcp.tool()(rooms.handlers.cancel_reservation)
    mcp.tool()(rooms.handlers.list_reservations)
    mcp.tool()(rooms.handlers.check_in)

    # Register mail tools
    mcp.tool()(mail.handlers.send_email)
    mcp.tool()(mail.handlers.create_draft)
    mcp.tool()(mail.handlers.update_draft)
    mcp.tool()(mail.handlers.send_draft)
    mcp.tool()(mail.handlers.delete_draft)
    mcp.tool()(mail.handlers.get_email)
    mcp.tool()(mail.handlers.get_thread)
    mcp.tool()(mail.handlers.search_emails)
    mcp.tool()(mail.handlers.reply_to_email)
    mcp.tool()(mail.handlers.forward_email)

    # Register directory tools
    mcp.tool()(directory.handlers.search_users)
    mcp.tool()(directory.handlers.get_user)
    mcp.tool()(directory.handlers.get_user_by_email)
    mcp.tool()(directory.handlers.get_user_by_employee_id)
    mcp.tool()(directory.handlers.resolve_identities)
    mcp.tool()(directory.handlers.search_groups)
    mcp.tool()(directory.handlers.get_group)
    mcp.tool()(directory.handlers.get_group_members)
    mcp.tool()(directory.handlers.get_org_chart)
    mcp.tool()(directory.handlers.get_direct_reports)

    # Register tasks tools
    mcp.tool()(tasks.handlers.create_task)
    mcp.tool()(tasks.handlers.get_task)
    mcp.tool()(tasks.handlers.update_task)
    mcp.tool()(tasks.handlers.delete_task)
    mcp.tool()(tasks.handlers.search_tasks)
    mcp.tool()(tasks.handlers.add_comment)
    mcp.tool()(tasks.handlers.assign_task)

    # Register docs tools
    mcp.tool()(docs.handlers.search_docs)
    mcp.tool()(docs.handlers.get_doc)
    mcp.tool()(docs.handlers.get_doc_permissions)
    mcp.tool()(docs.handlers.share_doc)
    mcp.tool()(docs.handlers.check_access)
    mcp.tool()(docs.handlers.revoke_access)

    # Register policies tools
    mcp.tool()(policies.handlers.get_working_hours)
    mcp.tool()(policies.handlers.list_holidays)
    mcp.tool()(policies.handlers.is_working_day)
    mcp.tool()(policies.handlers.get_rate_limits)
    mcp.tool()(policies.handlers.check_rate_limit)
    mcp.tool()(policies.handlers.get_spam_policy)
    mcp.tool()(policies.handlers.check_permission)
    mcp.tool()(policies.handlers.get_permissions)

    # Register utils tools
    mcp.tool()(ns_utils.handlers.convert_timezone)
    mcp.tool()(ns_utils.handlers.get_timezone_info)
    mcp.tool()(ns_utils.handlers.list_timezones)
    mcp.tool()(ns_utils.handlers.generate_ics)
    mcp.tool()(ns_utils.handlers.parse_ics)
    mcp.tool()(ns_utils.handlers.health_check)
    mcp.tool()(ns_utils.handlers.generate_idempotency_key)
    mcp.tool()(ns_utils.handlers.validate_idempotency_key)


# Register all namespaces
register_namespaces()


def main() -> None:
    """Main entry point."""
    settings = get_settings()
    logger.info("Starting Corp Collab MCP Server", {"version": "1.0.0", "transport": settings.transport})

    if settings.transport == "ws":
        logger.info(f"Starting WebSocket server on {settings.ws_host}:{settings.ws_port}")
        # Run with WebSocket transport
        mcp.run(transport="ws", host=settings.ws_host, port=settings.ws_port)
    else:
        logger.info("Starting with stdio transport")
        # Run with stdio transport (default)
        mcp.run()


if __name__ == "__main__":
    main()
