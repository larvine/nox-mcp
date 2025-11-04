"""CLI utility to interact with the Corp Collab FastMCP server.

This script provides a small test client around :class:`fastmcp.Client` so that
developers can quickly verify the MCP server behaviour without integrating a
full MCP runtime.

Usage examples::

    # List tools exposed by an HTTP server (default http://127.0.0.1:8765)
    python -m corp_collab_mcp.client list-tools

    # Call a specific tool with JSON arguments
    python -m corp_collab_mcp.client \
        --transport http://127.0.0.1:8765 \
        call-tool meetings.list_meetings --args '{"user_id": "abc", "start": "..."}'

The client supports any transport understood by :class:`fastmcp.Client`,
including HTTP endpoints, stdio subprocess configurations, or in-process
``FastMCP`` instances.
"""

from __future__ import annotations

if __name__ == "__main__" and (__package__ is None or __package__ == ""):
    # Allow `python path/to/client.py` to behave like `python -m corp_collab_mcp.client`
    import importlib
    import os
    import sys

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir in sys.path:
        sys.path.remove(script_dir)

    package_root = os.path.dirname(script_dir)
    if package_root not in sys.path:
        sys.path.insert(0, package_root)

    module = importlib.import_module("corp_collab_mcp.client")
    raise SystemExit(module.main())

import argparse
import asyncio
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Callable

from fastmcp import Client


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FastMCP test client")
    parser.add_argument(
        "--transport",
        default="http://127.0.0.1:8765",
        help=(
            "Transport configuration passed to fastmcp.Client. "
            "Can be an HTTP URL, a path/socket, or stdio JSON config."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="Default per-request timeout in seconds passed to the client.",
    )
    parser.add_argument(
        "--init-timeout",
        type=float,
        default=10.0,
        help="Timeout (seconds) for the initial connection handshake.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-tools", help="List available tools")
    list_parser.add_argument(
        "--json",
        action="store_true",
        help="Output the tool list as JSON instead of a readable table.",
    )

    call_parser = subparsers.add_parser("call-tool", help="Invoke a tool with arguments")
    call_parser.add_argument("name", help="Fully qualified tool name (e.g. meetings.list_meetings)")
    call_parser.add_argument(
        "--args",
        dest="args_json",
        default=None,
        help="JSON string with the tool arguments.",
    )
    call_parser.add_argument(
        "--args-file",
        type=Path,
        default=None,
        help="Read tool arguments from a JSON file.",
    )
    call_parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="Override the call timeout (seconds).",
    )
    call_parser.add_argument(
        "--raw",
        action="store_true",
        help="Return the raw MCP response (call_tool_mcp) instead of the simplified form.",
    )

    return parser


def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        return _normalize(asdict(value))
    if hasattr(value, "model_dump"):
        return _normalize(value.model_dump(mode="json"))
    if isinstance(value, dict):
        return {key: _normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_normalize(item) for item in value]
    return value


def _load_arguments(args_json: str | None, args_file: Path | None) -> dict[str, Any]:
    data: dict[str, Any] = {}
    if args_json:
        try:
            data = json.loads(args_json)
        except json.JSONDecodeError as exc:  # pragma: no cover - CLI error path
            raise SystemExit(f"Failed to parse --args JSON: {exc}") from exc

    if args_file:
        try:
            file_data = json.loads(args_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:  # pragma: no cover - CLI error path
            raise SystemExit(f"Failed to parse arguments file: {exc}") from exc
        if data:
            data.update(file_data)
        else:
            data = file_data

    if not isinstance(data, dict):
        raise SystemExit("Tool arguments must be a JSON object (dict)")
    return data


def _dump_json(payload: Any) -> None:
    print(json.dumps(_normalize(payload), ensure_ascii=False, indent=2))


async def _with_client(
    args: argparse.Namespace, callback: Callable[[Client, argparse.Namespace], Any]
) -> Any:
    client = Client(
        args.transport,
        timeout=args.timeout,
        init_timeout=args.init_timeout,
    )

    async with client:
        return await callback(client, args)


async def _cmd_list_tools(client: Client, args: argparse.Namespace) -> None:
    tools = await client.list_tools()
    if args.json:
        _dump_json([tool.model_dump(mode="json") for tool in tools])
        return

    if not tools:
        print("No tools registered on the server.")
        return

    for tool in tools:
        metadata = tool.model_dump()
        print(f"- {metadata['name']}")
        description = metadata.get("description")
        if description:
            print(f"  description: {description}")
        input_schema = metadata.get("inputSchema")
        if input_schema:
            print("  input schema:")
            print(json.dumps(input_schema, ensure_ascii=False, indent=4))
        print()


async def _cmd_call_tool(client: Client, args: argparse.Namespace) -> None:
    arguments = _load_arguments(args.args_json, args.args_file)

    call_timeout = args.timeout if args.timeout is not None else None

    if args.raw:
        result = await client.call_tool_mcp(
            name=args.name,
            arguments=arguments,
            timeout=call_timeout,
        )
        _dump_json(result.model_dump(mode="json"))
        if result.isError:
            raise SystemExit(1)
        return

    try:
        result = await client.call_tool(
            name=args.name,
            arguments=arguments,
            timeout=call_timeout,
        )
    except Exception as exc:  # pragma: no cover - runtime failure path
        print(f"Tool call failed: {exc}")
        raise SystemExit(1) from exc

    _dump_json(result)


async def _run_async(args: argparse.Namespace) -> None:
    command_map: dict[str, Callable[[Client, argparse.Namespace], Any]] = {
        "list-tools": _cmd_list_tools,
        "call-tool": _cmd_call_tool,
    }

    handler = command_map.get(args.command)
    if handler is None:  # pragma: no cover - argparse should prevent this
        raise SystemExit(f"Unknown command: {args.command}")

    await _with_client(args, handler)


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    asyncio.run(_run_async(args))


if __name__ == "__main__":
    main()
