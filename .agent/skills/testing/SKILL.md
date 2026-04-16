---
name: testing
description: >-
  Testing, coverage, and code quality workflow for the ai_demo project.
  Use this skill after every major code change, during refactors, or when
  debugging test failures. Covers tox, pytest, ruff, and coverage enforcement.
---

# Testing & Code Quality — Skill

## When to Use This Skill

- **After every major change**: Run the full quality suite to catch regressions
  before they reach a commit or pull request.
- **During refactors**: Update tests alongside the refactored code to keep
  expectations aligned with the new implementation.
- **When tests fail**: Follow the diagnosis workflow below to isolate and fix
  the root cause.

---

## Quick Reference

| Task | Command |
|---|---|
| Full quality suite (lint + format + tests) | `uv run tox` |
| Linting only | `uv run tox -e ruff-check` |
| Format check only | `uv run tox -e ruff-format` |
| Tests with coverage only | `uv run tox -e pytest` |
| Run tests directly (fast iteration) | `uv run pytest -v` |
| Run a single test file | `uv run pytest tests/test_flask.py -v` |
| Run a single test by name | `uv run pytest -v -k "test_health"` |
| Run tests with coverage (no tox) | `uv run pytest --cov=app --cov=mcp_server --cov-report=term-missing` |
| Auto-fix formatting | `uv run ruff format .` |
| Auto-fix lint issues | `uv run ruff check --fix .` |
| Install quality tools | `uv sync --group quality` |

---

## Workflow: After Every Major Change

Follow these steps after adding features, fixing bugs, or refactoring:

### Step 1 — Run the full tox suite

```bash
uv run tox
```

This runs three environments in order:

1. **`ruff-format`** — checks code formatting
2. **`ruff-check`** — linting for style, bugs, and import ordering
3. **`pytest`** — unit tests with coverage (fails if coverage < 80%)

### Step 2 — Fix any failures

| Failure type | Fix |
|---|---|
| **Format violation** | Run `uv run ruff format .` and re-run tox |
| **Lint error** | Run `uv run ruff check --fix .` for auto-fixable issues; manually fix the rest |
| **Test failure** | See *Diagnosing Test Failures* below |
| **Coverage below 80%** | Add tests for uncovered code paths; see *Improving Coverage* below |

### Step 3 — Confirm green

```bash
uv run tox
```

All three environments must pass before committing.

---

## Workflow: Updating Tests During a Refactor

When the implementation changes, tests must change with it. Follow this
checklist so tests stay aligned with the code:

1. **Identify affected tests** — After changing a function signature, route
   path, response shape, or tool return value, search for tests that assert
   on the old behavior.

2. **Update assertions** — Change expected values, status codes, and
   response keys to match the new implementation.

3. **Add new tests** — If the refactor introduces new branches, error paths,
   or endpoints, write tests for them.

4. **Remove obsolete tests** — Delete tests for removed functionality rather
   than commenting them out.

5. **Run the full suite** — `uv run tox` must pass before the refactor is
   considered complete.

### Example: Renaming a Route

If `/hello/<name>` is renamed to `/greet/<name>`:

- Update `test_flask.py`: change all `client.get("/hello/...")` calls to
  `client.get("/greet/...")`.
- Update `AGENTS.md` and any docs that reference the old path.
- Run `uv run tox` to verify.

---

## Diagnosing Test Failures

### 1. Read the failure output

```bash
uv run pytest -v --tb=long
```

`--tb=long` shows the full traceback. Look for:
- **AssertionError** — expected vs actual mismatch → update the test or fix
  the code.
- **ImportError** — missing dependency → `uv add <pkg>` or `uv sync`.
- **AttributeError / TypeError** — function signature changed → update the
  call in the test.

### 2. Run a single failing test

```bash
uv run pytest -v -k "test_create_item_missing_name"
```

Isolating one test speeds up the fix-verify loop.

### 3. Use pytest flags for more context

| Flag | Purpose |
|---|---|
| `--tb=long` | Full tracebacks |
| `--tb=short` | Compact tracebacks (default in tox) |
| `-s` | Show print/log output during tests |
| `--lf` | Re-run only last-failed tests |
| `-x` | Stop on first failure |
| `--pdb` | Drop into debugger on failure |

### 4. Check for state leaks

Each test should use the `client` fixture from `conftest.py`, which creates a
fresh `create_app()` instance. If tests pass alone but fail together, look for
shared mutable state outside fixtures.

---

## Improving Coverage

### Check what's uncovered

```bash
uv run pytest --cov=app --cov=mcp_server --cov-report=term-missing
```

The `Missing` column shows uncovered line numbers. Open the source file and
write tests that exercise those lines.

### Browse the HTML report

```bash
uv run pytest --cov=app --cov=mcp_server --cov-report=html
open htmlcov/index.html
```

Green lines are covered; red lines need tests.

### Coverage thresholds

- **Required minimum**: 80% (enforced by `--cov-fail-under=80` in tox)
- Coverage config lives in `tests/.coveragerc`
- Lines matching patterns in `exclude_lines` (e.g., `if __name__ == "__main__":`)
  are excluded from the report

---

## Tox Environment Details

| Environment | What it does | Key deps |
|---|---|---|
| `ruff-format` | Checks formatting (no auto-fix) | `ruff>=0.8.0` |
| `ruff-check` | Lints for errors, style, imports | `ruff>=0.8.0` |
| `pytest` | Runs tests + coverage gate | `pytest`, `pytest-cov`, `pytest-flask` |

Configuration lives in:
- `tox.ini` — environment definitions and pytest settings
- `tests/.coveragerc` — coverage source, omissions, and report options
- `pyproject.toml` — ruff lint/format rules, dependency groups

---

## Adding Tests for New Code

### New Flask endpoint

1. Add the route inside `create_app()` in `app.py`.
2. Add a test class in `tests/test_flask.py` with at least:
   - One happy-path test (200/201 response with correct body).
   - One error-path test (400/404/500 with appropriate status code).
3. Run `uv run tox -e pytest` to verify.

### New MCP tool

1. Add the `@mcp.tool()` function in `mcp_server.py`.
2. Import and call the function directly in `tests/test_mcp.py`.
3. Update `server_info()` to include the new tool name.
4. Run `uv run tox -e pytest` to verify.

---

## CI Integration

The tox environments are designed for CI pipelines. A typical pipeline stage:

```bash
uv sync --group quality
uv run tox -e ruff-check
uv run tox -e ruff-format
uv run tox -e pytest
```

All three must exit 0 for the build to pass.
