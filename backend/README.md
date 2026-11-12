# ArchPilot Backend

FastAPI backend for ArchPilot — an AI-assisted solution architecture workbench.

**Current scope: `M1-T01` only.** This package contains the application bootstrap and
a `GET /health` endpoint. There are no AI agents, LLM integrations, database,
validation rules or frontend code yet, by design.

## Requirements

- Python **3.12** (managed by `uv`; no system install required)
- [`uv`](https://docs.astral.sh/uv/) — package and dependency management

If `uv` is not on your `PATH`, it may be installed under a user site directory, e.g.
`~/Library/Python/3.9/bin/uv`. Add that directory to `PATH`, or install `uv` with the
official standalone installer.

## Setup

```bash
cd backend
uv sync
```

`uv sync` creates `.venv`, downloads Python 3.12 if needed, and installs both the
runtime and dev dependencies defined in `pyproject.toml`. The resolved versions are
locked in `uv.lock`.

## Run the API locally

```bash
cd backend
uv run uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}
```

No API key or external service is required for this milestone.

## Test

```bash
cd backend
uv run pytest
```

Tests use FastAPI's `TestClient` against a freshly created app instance, so they run
offline and never call a model provider.

## Lint and format

```bash
cd backend
uv run ruff check .
uv run ruff format --check .
```

To apply formatting automatically:

```bash
uv run ruff check --fix . && uv run ruff format .
```

## Layout

```text
backend/
├── app/
│   ├── main.py            # App factory + module-level ASGI `app`
│   ├── config.py          # Non-sensitive settings from environment
│   ├── api/health.py      # GET /health route
│   └── models/health.py   # HealthResponse contract
├── tests/
│   ├── conftest.py        # TestClient fixture
│   └── test_health.py     # Health endpoint smoke tests
├── pyproject.toml         # Dependencies, pytest and Ruff configuration
└── uv.lock                # Locked dependency versions
```

## Configuration

Non-secret settings are read from environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `ARCHPILOT_ENV` | `local` | Deployment/environment label |

Secrets (for example a future model-provider API key) must never be committed;
`.env` files are ignored by Git. No secret is required during `M1-T01`.
