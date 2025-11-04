"""Decorators to tag callables for MCP export."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, ParamSpec, TypeVar


P = ParamSpec("P")
T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class ExportMetadata:
    kind: str
    name: str
    options: dict[str, Any]


def _attach_metadata(kind: str, name: str, **meta: Any) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Attach export metadata to *kind* of callable."""

    def decorator(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        setattr(fn, "__export__", ExportMetadata(kind=kind, name=name, options=dict(meta)))
        return fn

    return decorator


def export_tool(name: str, **meta: Any) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Mark an async callable for tool registration."""

    return _attach_metadata("tool", name, **meta)


def export_resource(name: str, **meta: Any) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Mark an async callable for resource registration."""

    return _attach_metadata("resource", name, **meta)


__all__ = ["ExportMetadata", "export_tool", "export_resource"]
