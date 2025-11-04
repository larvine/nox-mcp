"""MCP Server implementation using FastMCP."""

import inspect
import pkgutil
from collections.abc import Callable
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from types import ModuleType

from fastmcp import FastMCP

from corp_collab_mcp.config import get_settings
from corp_collab_mcp.utils.logger import Logger

logger = Logger("server")

# Initialize FastMCP server
mcp = FastMCP("corp-collab-mcp")

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


def _iter_public_handlers(module: ModuleType) -> list[Callable[..., object]]:
    handlers: list[Callable[..., object]] = []
    for name, member in module.__dict__.items():
        if name.startswith("_"):
            continue
        if not (inspect.isfunction(member) or inspect.iscoroutinefunction(member)):
            continue
        if getattr(member, "__module__", "") != module.__name__:
            continue
        handlers.append(member)
    return handlers


def _discover_namespace_handler_modules() -> list[tuple[str, ModuleType]]:
    namespaces_pkg = import_module("corp_collab_mcp.namespaces")
    package_path = Path(namespaces_pkg.__file__).parent

    discovered: dict[str, ModuleType] = {}
    for module_info in pkgutil.iter_modules([str(package_path)]):
        if not module_info.ispkg or module_info.name.startswith("_"):
            continue

        namespace = module_info.name
        module_name = f"{namespaces_pkg.__name__}.{namespace}.{_HANDLERS_MODULE_NAME}"

        if find_spec(module_name) is None:
            logger.debug(
                "Skipping namespace without handlers module",
                {"namespace": namespace},
            )
            continue

        handlers_module = import_module(module_name)
        discovered[namespace] = handlers_module

    return sorted(discovered.items(), key=lambda item: _namespace_sort_key(item[0]))


# Import and register namespace tools
def register_namespaces() -> None:
    """Register all namespace tools discovered in the namespaces package."""

    total_tools_registered = 0
    namespaces_with_handlers = 0

    for namespace, handlers_module in _discover_namespace_handler_modules():
        handlers = _iter_public_handlers(handlers_module)

        if not handlers:
            logger.warning(
                "No handlers found for namespace",
                {"namespace": namespace},
            )
            continue

        namespaces_with_handlers += 1

        for handler in handlers:
            tool_name = f"{namespace}.{handler.__name__}"
            mcp.tool(name=tool_name)(handler)
            total_tools_registered += 1

    logger.info(
        "Registered namespace tools",
        {
            "namespaces": namespaces_with_handlers,
            "tools": total_tools_registered,
        },
    )


def main() -> None:
    """Main entry point."""
    settings = get_settings()
    logger.info("Starting Corp Collab MCP Server", {"version": "1.0.0"})
    mcp.run()


if __name__ == "__main__":
    # Register all namespaces
    register_namespaces()
    main()
