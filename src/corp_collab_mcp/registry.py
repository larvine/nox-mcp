"""Registration helpers for MCP tools and resources."""

from __future__ import annotations

import importlib
import inspect
from collections.abc import Awaitable, Callable, Iterable
from typing import Any, Final

from fastmcp import FastMCP

from corp_collab_mcp.common.export import ExportMetadata
from corp_collab_mcp.utils.logger import Logger


logger = Logger("registry")

ToolCallable = Callable[..., Awaitable[Any]]
ResourceCallable = Callable[..., Awaitable[Any]]

_DEFAULT_NAMESPACES: Final[tuple[str, ...]] = (
    "meetings",
    "rooms",
    "mail",
    "directory",
    "tasks",
    "docs",
    "policies",
    "utils",
)


def register_tool(app: FastMCP, fn: ToolCallable, *, name: str, **options: Any) -> None:
    """Register *fn* as an MCP tool on *app*."""

    logger.debug("Registering tool", {"name": name, "function": fn.__qualname__})
    app.register_tool(fn, name=name, **options)


def register_resource(app: FastMCP, fn: ResourceCallable, *, name: str, **options: Any) -> None:
    """Register *fn* as an MCP resource on *app*."""

    logger.debug("Registering resource", {"name": name, "function": fn.__qualname__})
    app.register_resource(fn, name=name, **options)


def _iter_exports(module: Any) -> Iterable[tuple[ToolCallable | ResourceCallable, ExportMetadata]]:
    for _, member in inspect.getmembers(module, inspect.iscoroutinefunction):
        metadata = getattr(member, "__export__", None)
        if isinstance(metadata, ExportMetadata):
            yield member, metadata


def register_all(app: FastMCP, namespaces: Iterable[str] | None = None) -> None:
    """Register all exported callables for the provided *namespaces*."""

    processed_tools: set[str] = set()
    processed_resources: set[str] = set()

    namespace_list = tuple(namespaces) if namespaces is not None else _DEFAULT_NAMESPACES

    for namespace in namespace_list:
        module_name = f"corp_collab_mcp.namespaces.{namespace}.handlers"
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.exception("Failed to import handlers module", {"namespace": namespace, "error": str(exc)})
            continue

        for fn, metadata in _iter_exports(module):
            name = metadata.name
            options = dict(metadata.options)

            if metadata.kind == "tool":
                if name in processed_tools:
                    logger.error("Duplicate tool registration skipped", {"tool": name})
                    continue
                register_tool(app, fn, name=name, **options)
                processed_tools.add(name)
            elif metadata.kind == "resource":
                if name in processed_resources:
                    logger.error("Duplicate resource registration skipped", {"resource": name})
                    continue
                register_resource(app, fn, name=name, **options)
                processed_resources.add(name)
            else:  # pragma: no cover - defensive branch
                logger.warning(
                    "Unknown export kind encountered", {"kind": metadata.kind, "name": name, "function": fn.__qualname__}
                )

    logger.info(
        "Completed registration",
        {
            "namespaces": len(namespace_list),
            "tools": len(processed_tools),
            "resources": len(processed_resources),
        },
    )


__all__ = ["register_tool", "register_resource", "register_all"]
