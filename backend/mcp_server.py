"""MCP server exposing the LLM Council as a tool."""

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from mcp.server.fastmcp import FastMCP
from .council import run_full_council

mcp = FastMCP("LLM Council")


@mcp.tool()
async def council_health() -> str:
    """Return non-sensitive MCP service metadata without invoking any models."""
    return (
        '{"status":"ok","service":"llm-council",'
        '"mode":"read-only","deliberation":false}'
    )


@mcp.tool()
async def council_query(prompt: str) -> str:
    """
    Submit a query to the LLM Council 3-stage deliberation process.

    Multiple frontier models respond independently (Stage 1), then anonymously
    peer-review and rank each other's responses (Stage 2), and a Chairman model
    synthesizes a final answer incorporating all perspectives and rankings (Stage 3).

    Returns the Chairman synthesis followed by peer rankings and individual model responses.
    """
    stage1, stage2, stage3, metadata = await run_full_council(prompt)

    if not stage1:
        return "Error: all council models failed to respond."

    lines = []

    lines.append("## Council Synthesis")
    lines.append(f"*Chairman: {stage3['model']}*\n")
    lines.append(stage3["response"])

    if metadata.get("aggregate_rankings"):
        lines.append("\n## Peer Rankings (lower avg = better)")
        for i, r in enumerate(metadata["aggregate_rankings"], 1):
            lines.append(
                f"{i}. **{r['model']}** — avg rank {r['average_rank']} "
                f"across {r['rankings_count']} evaluations"
            )

    lines.append("\n## Individual Responses")
    for result in stage1:
        lines.append(f"\n### {result['model']}")
        lines.append(result["response"])

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
