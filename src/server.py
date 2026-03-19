"""Health MCP Server — Medizinische Daten für AI-Agents."""

from mcp.server.fastmcp import FastMCP
from src.tools.health import register_health_tools

mcp = FastMCP(
    "Health MCP Server",
    instructions="Health and medical data — search drugs, check adverse events, find clinical trials, access WHO global health statistics. All data from public APIs, no key needed.",
)
register_health_tools(mcp)

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
