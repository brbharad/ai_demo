"""CLI utilities with Rich styling.

Provides banner display and enhanced console output for the ai_demo
Flask + FastMCP server.
"""

from __future__ import annotations

from typing import Literal

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console(stderr=True)

LOGO_ASCII = r"""
┏━╸╻  ┏━┓┏━┓╻┏    ┏┳┓┏━╸┏━┓
┣╸ ┃  ┣━┫┗━┓┣┻┓   ┃┃┃┃  ┣━┛
╹  ┗━╸╹ ╹┗━┛╹ ╹   ╹ ╹┗━╸╹
""".strip("\n")


def log_server_banner(
    server_name: str,
    transport: Literal["stdio", "http", "sse"] = "stdio",
    *,
    host: str | None = None,
    port: int | None = None,
    path: str | None = None,
) -> None:
    """Display a formatted startup banner with server information.

    Args:
        server_name: Name of the server being started.
        transport: Transport protocol in use.
        host: Bind address (for HTTP/SSE transports).
        port: Port number (for HTTP/SSE transports).
        path: URL path suffix (for HTTP/SSE transports).
    """
    logo_text = Text(LOGO_ASCII, style="bold green")

    info_table = Table.grid(padding=(0, 1))
    info_table.add_column(style="bold cyan", justify="left")
    info_table.add_column(style="white", justify="left")

    info_table.add_row("Server:", server_name)
    info_table.add_row("Transport:", transport.upper())

    if transport in ("http", "sse") and host and port:
        server_url = f"http://{host}:{port}"
        if path:
            server_url += f"/{path.lstrip('/')}"
        info_table.add_row("URL:", server_url)

    panel_content = Group(logo_text, "", info_table)
    panel = Panel(
        panel_content,
        title="ai_demo",
        title_align="left",
        border_style="dim",
        padding=(1, 4),
        expand=False,
    )
    console.print(Group("\n", panel, "\n"))


def log_startup_message() -> None:
    """Print a Rich-styled startup confirmation."""
    console.print("[bold green]Server started successfully.[/bold green]")
    console.print("[dim]Waiting for client connections ...[/dim]")


def log_shutdown_message() -> None:
    """Print a Rich-styled shutdown notice."""
    console.print("[bold red]Server shutting down ...[/bold red]")
