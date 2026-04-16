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

## Deployment Workflow

### Pre-deployment checklist

- [ ] Tests pass — `uv run pytest -v`
- [ ] No new linter warnings
- [ ] Changes reviewed and approved
- [ ] Dependencies up to date — `uv sync`

### Deploy steps

1. Run tests — `uv run pytest -v`
2. Review changes — `git diff`
3. Merge to main via pull request
4. Deploy to staging
5. Smoke test staging
6. Deploy to production
7. Smoke test production

### Post-deployment checklist

- [ ] Health check returns 200
- [ ] Smoke tests pass
- [ ] MCP server accessible on port 8000
- [ ] No errors in application logs

---

## Incident Response

### By symptom

| Symptom | First steps |
|---|---|
| 5xx errors | Check app logs for tracebacks → fix bug → redeploy |
| Connection refused | Check process running + port bound → restart → check firewall |
| Slow responses | Check CPU/memory/connections → scale up or optimize |
| MCP agent errors | Check port 8000, verify SSE transport → run `uv run pytest tests/test_mcp.py -v` |

### Severity levels

| Level | Example | Response time | Action |
|---|---|---|---|
| P1 | Service completely down | Immediate | Page on-call, start incident call |
| P2 | Partial outage / degraded | < 30 min | Investigate, escalate if needed |
| P3 | Non-critical prod bug | Next business day | File ticket, fix in sprint |
| P4 | Cosmetic / minor improvement | Backlog | Prioritize in grooming |

---

## Rollback

1. Switch to the previous known-good version
2. Run smoke tests to confirm rollback
3. Investigate the issue in a dev environment
4. Fix, test, and redeploy when ready

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
