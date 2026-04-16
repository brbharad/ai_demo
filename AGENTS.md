# ai_demo — Agent Instructions

## Commands

```bash
uv run python main.py          # Start both servers (Flask :5000 + MCP :8000)
uv run pytest -v                # Run full test suite — must pass before any commit
uv run pytest tests/test_flask.py -v   # Flask route tests only
uv run pytest -v -k "test_health"      # Single test by name
uv add <pkg>                    # Add a dependency (never use pip install)
uv sync                         # Restore environment from lockfile
```

---

## Project Context

Flask REST API + FastMCP server, single entry point (`main.py`), in-memory data store.

| Component | Tech | Port | Entry |
|-----------|------|------|-------|
| REST API | Flask 3.x | 5000 | `app.py` → `create_app()` |
| MCP Server | FastMCP 2.x | 8000 | `mcp_server.py` → `mcp` |
| Package Mgr | uv | — | `pyproject.toml` |
| Tests | pytest | — | `tests/` |
| Runtime | Python 3.12+ | — | `.python-version` |

For architecture details → `docs/architecture.md`
For dev environment setup → `docs/onboarding.md`

---

## File Map

```
app.py          ← Flask routes (all inside create_app())
mcp_server.py   ← MCP tools, resources, prompts
main.py         ← Entry point; Flask on daemon thread, MCP on main
tests/
├── test_flask.py   ← Route tests (status codes, response bodies)
└── test_mcp.py     ← MCP tool unit tests (call functions directly)
docs/
├── architecture.md ← System design (read before architectural changes)
└── onboarding.md   ← First-time setup guide
```

---

## Conventions

- Use `uv` package manager for python dependencies
- Type hints on every function parameter and return type
- `snake_case` for functions/variables; `PascalCase` for classes
- Lines ≤ 100 characters
- Match the style of the file you're editing — no wholesale reformats
- All Flask routes live inside `create_app()` — no module-level routes
- Every `@mcp.tool()` function must have a one-line docstring
- Use `logging` instead of `print()` in production code

---

## Constraints (Do NOT)

- No hardcoded secrets, tokens, or credentials — use environment variables
- No `pip install` — use `uv add <pkg>` or `uv sync`
- No bare `except:` — always catch specific exception types
- No mutable default arguments (e.g., `def f(items=[])`)
- No `debug=True` outside local dev; never in `main.py`
- No committing `.env` files
- No reformatting files you didn't functionally change

---

## Testing Rules

- Every new Flask route needs at least one happy-path test
- Every new `@mcp.tool()` needs a test in `test_mcp.py`
- Test at least one 4xx/5xx error path per route
- Each test creates its own `app` via `create_app()` — no shared state
- Do not modify fixture data shared across tests
- `uv run pytest -v` must exit 0 before any commit

---

## Adding New Code

### New Flask endpoint
1. Add route inside `create_app()` in `app.py`
2. Add test in `tests/test_flask.py`
3. Run `uv run pytest -v`

### New MCP tool
1. Add `@mcp.tool()` function in `mcp_server.py`
2. Add test in `tests/test_mcp.py`
3. Update the `server_info()` tool's tools list
4. Run `uv run pytest -v`

---

## Security

SonarQube for IDE runs continuous static analysis. Severity response:

| Level | Action |
|-------|--------|
| Blocker/Critical | Fix before opening a PR |
| Major | Fix in the same PR |
| Minor | Fix if you touched the file |

Never suppress Blocker/Critical without team review. When suppressing a
false positive, add an inline comment with the Sonar rule ID and reasoning.

---

## Skills & Reference Docs

- **Runbook** (`.agent/skills/runbook/SKILL.md`) — start/stop, health checks, smoke tests, incident response, rollback
- `docs/architecture.md` — read before making architectural decisions
- `docs/onboarding.md` — read when bootstrapping for the first time
