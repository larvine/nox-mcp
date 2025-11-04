"""MCP Server implementation using FastMCP."""

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
    for handler in [
        meetings.handlers.create_meeting,
        meetings.handlers.get_meeting,
        meetings.handlers.update_meeting,
        meetings.handlers.cancel_meeting,
        meetings.handlers.list_meetings,
        meetings.handlers.find_available_slots,
        meetings.handlers.get_availability,
    ]:
        mcp.tool(name=f"meetings.{handler.__name__}")(handler)

    # Register rooms tools
    for handler in [
        rooms.handlers.search_rooms,
        rooms.handlers.get_room,
        rooms.handlers.get_room_availability,
        rooms.handlers.reserve_room,
        rooms.handlers.cancel_reservation,
        rooms.handlers.list_reservations,
        rooms.handlers.check_in,
    ]:
        mcp.tool(name=f"rooms.{handler.__name__}")(handler)

    # Register mail tools
    for handler in [
        mail.handlers.send_email,
        mail.handlers.create_draft,
        mail.handlers.update_draft,
        mail.handlers.send_draft,
        mail.handlers.delete_draft,
        mail.handlers.get_email,
        mail.handlers.get_thread,
        mail.handlers.search_emails,
        mail.handlers.reply_to_email,
        mail.handlers.forward_email,
    ]:
        mcp.tool(name=f"mail.{handler.__name__}")(handler)

    # Register directory tools
    for handler in [
        directory.handlers.search_users,
        directory.handlers.get_user,
        directory.handlers.get_user_by_email,
        directory.handlers.get_user_by_employee_id,
        directory.handlers.resolve_identities,
        directory.handlers.search_groups,
        directory.handlers.get_group,
        directory.handlers.get_group_members,
        directory.handlers.get_org_chart,
        directory.handlers.get_direct_reports,
    ]:
        mcp.tool(name=f"directory.{handler.__name__}")(handler)

    # Register tasks tools
    for handler in [
    tasks.handlers.create_task,
    tasks.handlers.get_task,
    tasks.handlers.update_task,
    tasks.handlers.delete_task,
    tasks.handlers.search_tasks,
    tasks.handlers.add_comment,
    tasks.handlers.assign_task,
    ]:
        mcp.tool(name=f"tasks.{handler.__name__}")(handler)

    # Register docs tools
    for handler in [
    docs.handlers.search_docs,
    docs.handlers.get_doc,
    docs.handlers.get_doc_permissions,
    docs.handlers.share_doc,
    docs.handlers.check_access,
    docs.handlers.revoke_access,
    ]:
        mcp.tool(name=f"docs.{handler.__name__}")(handler)

    # Register policies tools
    for handler in [
    policies.handlers.get_working_hours,
    policies.handlers.list_holidays,
    policies.handlers.is_working_day,
    policies.handlers.get_rate_limits,
    policies.handlers.check_rate_limit,
    policies.handlers.get_spam_policy,
    policies.handlers.check_permission,
    policies.handlers.get_permissions,
    ]:
        mcp.tool(name=f"policies.{handler.__name__}")(handler)

    # Register utils tools
    for handler in [
    ns_utils.handlers.convert_timezone,
    ns_utils.handlers.get_timezone_info,
    ns_utils.handlers.list_timezones,
    ns_utils.handlers.generate_ics,
    ns_utils.handlers.parse_ics,
    ns_utils.handlers.health_check,
    ns_utils.handlers.generate_idempotency_key,
    ns_utils.handlers.validate_idempotency_key,
    ]:
        mcp.tool(name=f"utils.{handler.__name__}")(handler)


def main() -> None:
    """Main entry point."""
    settings = get_settings()
    logger.info("Starting Corp Collab MCP Server", {"version": "1.0.0"})
    mcp.run()


if __name__ == "__main__":
    # Register all namespaces
    register_namespaces()
    main()
