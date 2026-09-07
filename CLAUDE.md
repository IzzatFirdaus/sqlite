# CLAUDE.md — CLI Quickstart for LLM Tooling

> **Use this file** when an LLM-based CLI (Claude Code, Gemini CLI, aider, etc.) needs to operate on this repo. It is optimized for fast context loading, not for humans.

---

## 1. One-Line Summary

FastAPI + SQLModel + SQLite single-file CRUD API, scoped to one `Item` resource.

## 2. Environment Setup (Windows / PowerShell)

```powershell
cd d:\Projects\sqlite-fastapi
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Cross-platform equivalent (bash):

```bash
cd /path/to/sqlite-fastapi
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Common Commands

| Purpose | Command |
| :--- | :--- |
| Run dev server (hot reload) | `fastapi dev main.py` |
| Run prod-style server | `uvicorn main:app --host 0.0.0.0 --port 8000` |
| Open interactive docs | `http://127.0.0.1:8000/docs` |
| Open raw OpenAPI schema | `http://127.0.0.1:8000/openapi.json` |
| Run all tests | `pytest -q` |
| Run only unit tests | `pytest -q -m unit` |
| Lint | `ruff check .` |
| Auto-format | `ruff format .` |
| Byte-compile sanity check | `python -m py_compile main.py` |
| Reset local DB | `Remove-Item database.db` (then restart server) |

## 4. Path Aliases & Key Locations

| Alias | Path | Purpose |
| :--- | :--- | :--- |
| `@root` | project root | entrypoint and config |
| `@app` | `app/` | application package |
| `@api` | `app/api/v1/endpoints/` | route handlers |
| `@models` | `app/models/` | SQLModel table classes |
| `@schemas` | `app/schemas/` | request/response DTOs |
| `@services` | `app/services/` | business rules |
| `@repos` | `app/repositories/` | DB access |
| `@tests` | `tests/` | pytest suite |
| `@docs` | `PRD.md`, `ARCHITECTURE.md`, `ARCHITECTURE-ESSENTIALS.md`, `AGENTS.md` | documentation |

## 5. Repository Map (post-scaffold)

```
sqlite-fastapi/
├── main.py
├── requirements.txt
├── README.md
├── PRD.md
├── ARCHITECTURE.md
├── ARCHITECTURE-ESSENTIALS.md
├── AGENTS.md
├── CLAUDE.md
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── logging_config.py
│   ├── exceptions.py
│   ├── models/{__init__.py, base.py, item.py}
│   ├── schemas/{__init__.py, item_create.py, item_update.py, item_read.py}
│   ├── repositories/{__init__.py, item_repository.py}
│   ├── services/{__init__.py, item_service.py}
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/{__init__.py, health.py, items.py}
│   └── core/{__init__.py, pagination.py}
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_health.py
    ├── test_items_crud.py
    └── test_items_validation.py
```

## 6. Endpoint Cheatsheet

| Method | Path | Purpose |
| :--- | :--- | :--- |
| GET | `/health` | Liveness |
| POST | `/api/v1/items/` | Create |
| GET | `/api/v1/items/?skip=0&limit=50&is_available=true` | List |
| GET | `/api/v1/items/{id}` | Read |
| PUT | `/api/v1/items/{id}` | Replace |
| PATCH | `/api/v1/items/{id}` | Partial update |
| DELETE | `/api/v1/items/{id}` | Delete |

## 7. Environment Variables

| Name | Default | Notes |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite:///./database.db` | Override for tests (`sqlite:///:memory:`). |
| `SQL_ECHO` | `false` | Set `true` to log SQL. |
| `LOG_LEVEL` | `INFO` | Standard library levels. |
| `APP_NAME` | `FastAPI + SQLite Persistence API` | OpenAPI title. |
| `CORS_ALLOW_ORIGINS` | `*` | Comma-separated list. |

## 8. LLM Operating Hints

- **Preferred entry point for edits**: `app/api/v1/endpoints/items.py` for routes, `app/services/item_service.py` for rules.
- **Persistence source of truth**: `app/database.py`. Avoid touching it unless adding `lifespan` behavior.
- **Tests are the contract.** If you change a route, update or add tests in `tests/test_items_*.py`.
- **Docs to update after feature work**: `README.md` (endpoint table), `ARCHITECTURE.md` (API surface table if changed), `ARCHITECTURE-ESSENTIALS.md` (only if rules change).
- **Do not** edit `requirements.txt` without an explicit request; the project intentionally has a tight dependency set.