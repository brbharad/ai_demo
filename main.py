"""Entry point — runs Flask and the FastMCP server concurrently.

Flask REST API  →  http://0.0.0.0:5000
MCP (SSE)       →  http://0.0.0.0:8000/sse
"""

from __future__ import annotations

import threading

from app import create_app
from mcp_server import mcp


def _run_flask() -> None:
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, use_reloader=False, debug=False)


def main() -> None:
    print("Starting Flask REST API  →  http://0.0.0.0:5000")
    flask_thread = threading.Thread(target=_run_flask, daemon=True)
    flask_thread.start()

    print("Starting FastMCP (SSE)   →  http://0.0.0.0:8000/sse")
    mcp.run(transport="sse", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
