"""FastMCP server — tools, resources, and prompts.

Run standalone:
    uv run python mcp_server.py

Or imported by main.py to run alongside Flask.
"""

from __future__ import annotations

from fastmcp import FastMCP

mcp = FastMCP(
    name="Hello World MCP",
    instructions=("A simple hello-world MCP server demonstrating tools, resources, and prompts."),
)


# ── Tools ─────────────────────────────────────────────────────────────────────


@mcp.tool()
def hello(name: str = "World") -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Greetings from FastMCP."


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b


@mcp.tool()
def server_info() -> dict:
    """Return basic information about this MCP server."""
    return {
        "name": "Hello World MCP",
        "version": "0.1.0",
        "tools": ["hello", "add", "server_info"],
        "resources": ["greeting://{name}"],
        "prompts": ["hello_prompt"],
    }


# ── Resources ─────────────────────────────────────────────────────────────────


@mcp.resource("greeting://{name}")
def greeting_resource(name: str) -> str:
    """A personalised greeting resource."""
    return f"Hello, {name}! This is a FastMCP resource."


# ── Prompts ───────────────────────────────────────────────────────────────────


@mcp.prompt()
def hello_prompt(name: str = "World") -> str:
    """Generate a friendly greeting prompt."""
    return f"Please greet {name} warmly and introduce yourself as a helpful AI assistant."


if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
