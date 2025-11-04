"""MCP Server implementation using FastMCP."""

import pkgutil
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path

from corp_collab_mcp.app import mcp
from corp_collab_mcp.config import get_settings
from corp_collab_mcp.utils.logger import Logger

logger = Logger("server")

_HANDLERS_MODULE_NAME = "handlers"
_DEFAULT_NAMESPACE_ORDER = (
    "meetings",
    "rooms",
    "mail",
    "directory",
    "tasks",
    "docs",
    "policies",
    "utils",
)


def _namespace_sort_key(namespace: str) -> tuple[int, int | str]:
    try:
        return (0, _DEFAULT_NAMESPACE_ORDER.index(namespace))
    except ValueError:
        return (1, namespace)


def _discover_namespace_handler_modules() -> list[str]:
    namespaces_pkg = import_module("corp_collab_mcp.namespaces")
    package_path = Path(namespaces_pkg.__file__).parent

    discovered: list[str] = []
    for module_info in pkgutil.iter_modules([str(package_path)]):
        if not module_info.ispkg or module_info.name.startswith("_"):
            continue

        namespace = module_info.name
        module_name = f"{namespaces_pkg.__name__}.{namespace}.{_HANDLERS_MODULE_NAME}"

        if find_spec(module_name) is None:
            logger.debug("Skipping namespace without handlers module", {"namespace": namespace})
            continue

        discovered.append(module_name)

    discovered.sort(key=lambda module_name: _namespace_sort_key(module_name.split(".")[-2]))
    return discovered


def register_namespaces() -> None:
    modules = _discover_namespace_handler_modules()
    for module_name in modules:
        try:
            import_module(module_name)
        except Exception as exc:
            logger.exception(
                "Failed to import handlers module",
                {"module": module_name, "error": str(exc)},
            )

    logger.info("Registered namespace handlers", {"modules": len(modules)})


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
