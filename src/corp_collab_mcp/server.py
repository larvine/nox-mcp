"""MCP Server implementation using FastMCP."""

from fastmcp import FastMCP

from corp_collab_mcp.config import get_settings
from corp_collab_mcp.registry import register_all
from corp_collab_mcp.utils.logger import Logger

logger = Logger("server")

# Initialize FastMCP server
mcp = FastMCP("corp-collab-mcp")


def register_namespaces() -> None:
    register_all(mcp)


def main() -> None:
    """Main entry point."""
    settings = get_settings()
    logger.info("Starting Corp Collab MCP Server", {"version": "1.0.0", "transport": settings.transport})

    # Register all namespaces
    register_namespaces()

    logger.info("Registered successfully", {"version": "1.0.0"})

    if settings.transport == "http":
        logger.info(f"Starting HTTP server on {settings.ws_host}:{settings.ws_port}")
        # Run with HTTP transport (FastMCP built-in HTTP server)
        mcp.run(transport="http", host=settings.ws_host, port=settings.ws_port)
    else:
        logger.info("Starting with stdio transport")
        # Run with stdio transport (default)
        mcp.run()


if __name__ == "__main__":
    main()
