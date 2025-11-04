"""Application-wide FastMCP instance."""

from fastmcp import FastMCP


mcp = FastMCP("corp-collab-mcp")


__all__ = ["mcp"]
