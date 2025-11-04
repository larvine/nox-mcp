"""MCP tool handlers for directory namespace."""

from corp_collab_mcp.app import mcp
from corp_collab_mcp.utils.logger import Logger

from .types import (
    DirectoryGroup,
    DirectoryUser,
    GetOrgChartRequest,
    OrgChartNode,
    ResolvedIdentity,
    ResolveIdentitiesRequest,
    SearchGroupsRequest,
    SearchUsersRequest,
)

logger = Logger("directory")


@mcp.tool(name="directory.search_users", description="Search for users in the directory.")
async def search_users(params: SearchUsersRequest) -> list[DirectoryUser]:
    """
    directory.searchUsers
    Search for users in the directory.
    """
    logger.info("Searching users", {"query": params.query})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.searchUsers not yet implemented")


@mcp.resource(name="directory.get_user", description="Get a user by their directory identifier.")
async def get_user(user_id: str) -> DirectoryUser:
    """
    directory.getUser
    Get user by ID.
    """
    logger.info("Getting user", {"user_id": user_id})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.getUser not yet implemented")


@mcp.resource(name="directory.get_user_by_email", description="Get a user by their email address.")
async def get_user_by_email(email: str) -> DirectoryUser:
    """
    directory.getUserByEmail
    Get user by email address.
    """
    logger.info("Getting user by email", {"email": email})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.getUserByEmail not yet implemented")


@mcp.resource(name="directory.get_user_by_employee_id", description="Get a user by their employee ID.")
async def get_user_by_employee_id(employee_id: str) -> DirectoryUser:
    """
    directory.getUserByEmployeeId
    Get user by employee ID.
    """
    logger.info("Getting user by employee ID", {"employee_id": employee_id})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.getUserByEmployeeId not yet implemented")


@mcp.tool(
    name="directory.resolve_identities",
    description="Resolve identifiers to canonical directory identities.",
)
async def resolve_identities(params: ResolveIdentitiesRequest) -> list[ResolvedIdentity]:
    """
    directory.resolveIdentities
    Resolve multiple identifiers (emails, employee IDs, aliases) to canonical user/group IDs.
    This is critical for normalizing user inputs across the system.
    """
    logger.info("Resolving identities", {"count": len(params.identifiers)})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.resolveIdentities not yet implemented")


@mcp.tool(name="directory.search_groups", description="Search for groups or teams.")
async def search_groups(params: SearchGroupsRequest) -> list[DirectoryGroup]:
    """
    directory.searchGroups
    Search for groups/teams.
    """
    logger.info("Searching groups", {"query": params.query})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.searchGroups not yet implemented")


@mcp.resource(name="directory.get_group", description="Get a group by its identifier.")
async def get_group(group_id: str) -> DirectoryGroup:
    """
    directory.getGroup
    Get group by ID.
    """
    logger.info("Getting group", {"group_id": group_id})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.getGroup not yet implemented")


@mcp.resource(name="directory.get_group_members", description="List members of a group.")
async def get_group_members(group_id: str) -> list[DirectoryUser]:
    """
    directory.getGroupMembers
    Get members of a group.
    """
    logger.info("Getting group members", {"group_id": group_id})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.getGroupMembers not yet implemented")


@mcp.resource(
    name="directory.get_org_chart",
    description="Retrieve the organizational chart for a user.",
)
async def get_org_chart(params: GetOrgChartRequest) -> OrgChartNode:
    """
    directory.getOrgChart
    Get organizational chart for a user.
    """
    logger.info("Getting org chart", {"user_id": params.user_id, "depth": params.depth})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.getOrgChart not yet implemented")


@mcp.resource(name="directory.get_direct_reports", description="Get direct reports for a manager.")
async def get_direct_reports(user_id: str) -> list[DirectoryUser]:
    """
    directory.getDirectReports
    Get direct reports for a manager.
    """
    logger.info("Getting direct reports", {"user_id": user_id})
    # TODO: Implement actual API call
    raise NotImplementedError("directory.getDirectReports not yet implemented")
