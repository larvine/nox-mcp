"""MCP Server implementation using FastMCP."""

import inspect
import pkgutil
from collections.abc import Callable
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path

from fastmcp import FastMCP

from corp_collab_mcp.config import get_settings
from corp_collab_mcp.utils.logger import Logger
from types import ModuleType

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
    # __all__이 있으면 그 목록만 신뢰(명시적 공개)
    if hasattr(module, "__all__"):
        out: list[Callable[..., object]] = []
        for name in getattr(module, "__all__"):  # type: ignore
            member = getattr(module, name, None)
            if inspect.isfunction(member) or inspect.iscoroutinefunction(member):
                out.append(member)
        return out

    # 없으면 규칙 기반 추출
    handlers: list[Callable[..., object]] = []
    for name, member in module.__dict__.items():
        if name.startswith("_"):
            continue
        if not (inspect.isfunction(member) or inspect.iscoroutinefunction(member)):
            continue
        # 해당 모듈에서 정의된 함수만 노출(바인딩된 import 함수 제외)
        if getattr(member, "__module__", "") != module.__name__:
            continue
        handlers.append(member)
    # 등록 순서 안정화
    handlers.sort(key=lambda f: f.__name__)
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

        try:
            if find_spec(module_name) is None:
                logger.debug("Skipping namespace without handlers module", {"namespace": namespace})
                continue
            handlers_module = import_module(module_name)
        except Exception as e:
            logger.exception(
                "Failed to import handlers module", {"namespace": namespace, "error": str(e)}
            )
            continue

        discovered[namespace] = handlers_module

    return sorted(discovered.items(), key=lambda item: _namespace_sort_key(item[0]))


def register_namespaces() -> None:
    total_tools_registered = 0
    namespaces_with_handlers = 0
    seen_tools: set[str] = set()

    for namespace, handlers_module in _discover_namespace_handler_modules():
        try:
            handlers = _iter_public_handlers(handlers_module)
        except Exception as e:
            logger.exception(
                "Failed to enumerate handlers", {"namespace": namespace, "error": str(e)}
            )
            continue

        if not handlers:
            logger.warning("No handlers found for namespace", {"namespace": namespace})
            continue

        namespaces_with_handlers += 1

        for handler in handlers:
            tool_name = f"{namespace}.{handler.__name__}"
            if tool_name in seen_tools:
                logger.error("Duplicate tool name detected; skipping", {"tool": tool_name})
                continue
            mcp.tool(name=tool_name)(handler)
            seen_tools.add(tool_name)
            total_tools_registered += 1

    logger.info(
        "Registered namespace tools",
        {"namespaces": namespaces_with_handlers, "tools": total_tools_registered},
    )


def main() -> None:
    """Main entry point."""
    settings = get_settings()
    logger.info("Starting Corp Collab MCP Server", {"version": "1.0.0"})

    # Register all namespaces
    register_namespaces()

    logger.info("Registered successfully", {"version": "1.0.0"})
    mcp.run()


if __name__ == "__main__":
    main()
