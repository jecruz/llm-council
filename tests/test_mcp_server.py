"""Focused tests for the LLM Council MCP surface."""

import asyncio
import json

from backend.mcp_server import council_health, mcp


def test_council_health_returns_non_sensitive_read_only_metadata() -> None:
    """The health probe must not expose configuration or trigger deliberation."""
    result = json.loads(asyncio.run(council_health()))

    assert result == {
        "status": "ok",
        "service": "llm-council",
        "mode": "read-only",
        "deliberation": False,
    }


def test_council_health_is_registered_as_an_mcp_tool() -> None:
    """The health probe must be discoverable through the MCP server."""
    tools = asyncio.run(mcp.list_tools())

    assert {tool.name for tool in tools} == {"council_health", "council_query"}
