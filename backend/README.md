# ArchPilot Backend

FastAPI backend for ArchPilot — an AI-assisted solution architecture workbench.

**Current scope: `M1-T01` and `M1-T02`.** The package contains the application
bootstrap, a `GET /health` endpoint, the project input contract, the discovery state
vocabulary, and a loader for the capability vocabulary. There are no AI agents, LLM
integrations, database, validation rules, API routes for projects, or frontend code yet,
by design.

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

## Contracts and fixtures

- `app/models/project.py` — `ProjectCreate`, the only way customer text enters the
  system. Blank or oversized input is rejected after whitespace trimming.
- `app/models/enums.py` — the five discovery-phase states (requirement kind, knowledge
  status, question priority, question status, discovery readiness).
- `app/models/limits.py` — contract character limits (title 120, brief 20,000, answer
  4,000).
- `../catalog/capabilities.json` — the versioned, 14-entry capability vocabulary shared
  by both AI roles. Loaded through `app/catalog/vocabulary.py`, which rejects duplicate
  IDs, duplicate aliases and alias/ID clashes.
- `../examples/synthetic-briefs/` — three fabricated customer briefs used as test and
  demo inputs. Never add real customer or company material here.

## Layout

```text
backend/
├── app/
│   ├── main.py                    # App factory + module-level ASGI `app`
│   ├── config.py                  # Non-sensitive settings from environment
│   ├── api/health.py              # GET /health route
│   ├── catalog/vocabulary.py      # Capability vocabulary loader
│   └── models/
│       ├── health.py              # HealthResponse contract
│       ├── limits.py              # Contract character limits
│       ├── enums.py               # Discovery state vocabulary
│       └── project.py             # ProjectCreate input contract
├── tests/
│   ├── conftest.py                # TestClient fixture
│   ├── test_health.py             # Health endpoint smoke tests
│   ├── test_project_schema.py     # Input contract (blank/oversized/multilingual)
│   ├── test_capability_vocabulary.py
│   └── test_synthetic_briefs.py   # Fixtures are valid project inputs
├── pyproject.toml                 # Dependencies, pytest and Ruff configuration
└── uv.lock                        # Locked dependency versions

catalog/capabilities.json          # Versioned capability vocabulary (repo root)
examples/synthetic-briefs/          # Fabricated customer briefs
```

## Configuration

Non-secret settings are read from environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `ARCHPILOT_ENV` | `local` | Deployment/environment label |

Secrets (for example a future model-provider API key) must never be committed;
`.env` files are ignored by Git. No secret is required through `M1-T02`.
