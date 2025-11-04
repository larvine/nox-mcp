"""Types for directory namespace."""

from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class GroupType(str, Enum):
    """Group type."""

    TEAM = "team"
    DISTRIBUTION_LIST = "distribution_list"
    SECURITY = "security"
    DYNAMIC = "dynamic"


class DirectoryUser(BaseModel):
    """User directory entry."""

    id: str
    email: EmailStr
    alternate_emails: list[EmailStr] | None = None
    employee_id: str | None = None
    name: str
    display_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    department: str | None = None
    title: str | None = None
    manager: "DirectoryUser | None" = None
    office_location: str | None = None
    phone: str | None = None
    mobile_phone: str | None = None
    photo_url: str | None = None
    is_active: bool = True
    aliases: list[str] | None = None
    metadata: dict[str, str] | None = None


class DirectoryGroup(BaseModel):
    """Group/Team directory entry."""

    id: str
    name: str
    display_name: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    members: list[DirectoryUser]
    member_count: int = Field(..., ge=0)
    owners: list[DirectoryUser] | None = None
    type: GroupType
    is_active: bool = True
    metadata: dict[str, str] | None = None


class ResolvedIdentity(BaseModel):
    """Identity resolution result."""

    input: str
    resolved: bool
    user: DirectoryUser | None = None
    group: DirectoryGroup | None = None
    type: str | None = Field(None, pattern="^(user|group|external)$")
    error: str | None = None


class SearchUsersRequest(BaseModel):
    """Request to search for users."""

    query: str | None = None
    department: str | None = None
    title: str | None = None
    location: str | None = None
    is_active: bool | None = None
    limit: int = Field(default=20, ge=1, le=100)


class SearchGroupsRequest(BaseModel):
    """Request to search for groups."""

    query: str | None = None
    type: GroupType | None = None
    limit: int = Field(default=20, ge=1, le=100)


class ResolveIdentitiesRequest(BaseModel):
    """Request to resolve multiple identifiers."""

    identifiers: list[str] = Field(..., min_items=1)
    include_inactive: bool = False


class GetOrgChartRequest(BaseModel):
    """Request to get organizational chart."""

    user_id: str
    depth: int = Field(default=2, ge=1, le=10)


class OrgChartNode(BaseModel):
    """Organizational chart node."""

    user: DirectoryUser
    manager: "OrgChartNode | None" = None
    direct_reports: list["OrgChartNode"] = []


# Update forward references
DirectoryUser.model_rebuild()
OrgChartNode.model_rebuild()
