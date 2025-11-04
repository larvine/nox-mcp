"""MCP tool handlers for docs namespace."""

from corp_collab_mcp.common.export import export_tool
from corp_collab_mcp.utils.logger import Logger

from .types import Document, DocumentPermission, SearchDocsRequest, ShareDocRequest

logger = Logger("docs")


@export_tool(
    "docs.search_docs",
    description="Search for documents by query.",
)
async def search_docs(params: SearchDocsRequest) -> list[Document]:
    """
    docs.search
    Search for documents.
    """
    logger.info("Searching documents", {"query": params.query})
    # TODO: Implement actual API call
    raise NotImplementedError("docs.search not yet implemented")


@export_tool(
    "docs.get_doc",
    description="Get a document by its identifier.",
)
async def get_doc(doc_id: str) -> Document:
    """
    docs.get
    Get document by ID.
    """
    logger.info("Getting document", {"doc_id": doc_id})
    # TODO: Implement actual API call
    raise NotImplementedError("docs.get not yet implemented")


@export_tool(
    "docs.get_doc_permissions",
    description="Fetch the permission entries for a document.",
)
async def get_doc_permissions(doc_id: str) -> list[DocumentPermission]:
    """
    docs.getPermissions
    Get document permissions.
    """
    logger.info("Getting document permissions", {"doc_id": doc_id})
    # TODO: Implement actual API call
    raise NotImplementedError("docs.getPermissions not yet implemented")


@export_tool(
    "docs.share_doc",
    description="Share a document with users or groups.",
)
async def share_doc(params: ShareDocRequest) -> Document:
    """
    docs.share
    Share a document with users/groups.
    """
    logger.info("Sharing document", {"doc_id": params.document_id})
    # TODO: Implement actual API call
    raise NotImplementedError("docs.share not yet implemented")


@export_tool(
    "docs.check_access",
    description="Check whether a user has access to a document.",
)
async def check_access(doc_id: str, user_id: str) -> bool:
    """
    docs.checkAccess
    Check if a user has access to a document.
    """
    logger.info("Checking document access", {"doc_id": doc_id, "user_id": user_id})
    # TODO: Implement actual API call
    raise NotImplementedError("docs.checkAccess not yet implemented")


@export_tool(
    "docs.revoke_access",
    description="Revoke a user's access to a document.",
)
async def revoke_access(doc_id: str, user_id: str) -> None:
    """
    docs.revokeAccess
    Revoke access to a document.
    """
    logger.info("Revoking document access", {"doc_id": doc_id, "user_id": user_id})
    # TODO: Implement actual API call
    raise NotImplementedError("docs.revokeAccess not yet implemented")
