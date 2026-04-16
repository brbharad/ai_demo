---
name: runbook
description: >-
  Operations playbook for running, deploying, health-checking, and troubleshooting
  the ai_demo project. Use when the user asks to start the service, run a
  smoke test, deploy, check health, respond to incidents, roll back, or debug
  connection/server errors.
---

# Runbook — Operations Skill

Operational reference for deployments, health checks, incident response, and
day-to-day service management.

---

## Starting the Service

```bash
# Full stack (Flask + MCP)
uv run python main.py

# Flask only
uv run python app.py

# MCP server only
uv run python mcp_server.py
```

Expected startup output:

```
Starting Flask REST API  →  http://0.0.0.0:5000
Starting FastMCP (SSE)   →  http://0.0.0.0:8000/sse
```

---

## Health Check

```bash
curl -s http://localhost:5000/health | python -m json.tool
```

If the health check fails, follow this sequence:

1. **Check the process** — `ps aux | grep main.py`
2. **Check port binding** — `lsof -i :5000`
3. **Restart** — `uv run python main.py`
4. **Re-check** — run the health check curl again

---

## Smoke Tests

Run after every deployment or service restart:

```bash
curl -s http://localhost:5000/health | python -m json.tool
curl -s http://localhost:5000/hello/CiscoIT | python -m json.tool
curl -s http://localhost:5000/items | python -m json.tool
curl -s -X POST http://localhost:5000/items \
     -H 'Content-Type: application/json' \
     -d '{"name": "test-deploy", "value": 1}' | python -m json.tool
```

All four must return valid JSON with no errors.

---

## Quick Command Reference

| Task | Command |
|---|---|
| Install dependencies | `uv sync` |
| Install with dev tools | `uv sync --group dev` |
| Run full stack | `uv run python main.py` |
| Run tests | `uv run pytest -v` |
| Check port listener | `lsof -i :5000` |
| View recent logs | Check stdout of the running process |
