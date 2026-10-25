"""The MCP entry point must declare its supported SDK major."""
from pathlib import Path


def test_mcp_dependency_is_bounded_to_supported_major():
    """Keep a future incompatible MCP major out of the runtime contract."""
    assert '"mcp>=1.0.0,<2"' in Path('pyproject.toml').read_text()
