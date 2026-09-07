# Architecture Specification

> **Project:** SQLite + FastAPI Persistence API
> **Status:** Draft v1.0
> **Companion document:** `PRD.md`
> **Purpose:** Single source of truth for technical design.

---

## 1. Tech Stack

| Layer | Technology | Version | Rationale |
| :--- | :--- | :--- | :--- |
| Language | Python | 3.10+ | Matches FastAPI/SQLModel minimum. |
| Web framework | FastAPI | latest stable | Async-friendly, OpenAPI built-in, Pydantic-native. |
| ASGI server | Uvicorn | latest stable | Default for FastAPI dev (`fastapi dev`) and prod. |
| ORM | SQLModel | latest stable | Combines Pydantic + SQLAlchemy; reduces ceremony. |
| Database driver | SQLAlchemy sqlite3 (stdlib) | bundled | Zero-install SQLite driver. |
| Database | SQLite | 3.x | Embedded, file-based, zero-config persistence. |
| Validation | Pydantic v2 | via SQLModel | Field validation + serialization. |
| Logging | stdlib `logging` | stdlib | No extra dependency required. |
| Testing | pytest + httpx | latest | Standard FastAPI testing stack. |

## 2. High-Level System Diagram

```
+----------+      HTTP/JSON      +-----------------+      SQL       +-----------+
|  Client  | <-----------------> |   FastAPI App   | <-----------> | SQLite DB |
+----------+                     |  (Uvicorn ASGI) |               |  file.db  |
                                 +-----------------+               +-----------+
                                          |
                                          v
                                  +-----------------+
                                  |   SQLModel ORM  |
                                  +-----------------+
```

Single-process, single-threaded-by-default SQLite (with `check_same_thread=False` for FastAPI's threadpool).

## 3. Directory Layout

```
sqlite-fastapi/
├── main.py                       # FastAPI entrypoint (composition root)
├── requirements.txt              # Pinned dependencies
├── README.md                     # Human-facing quickstart
├── PRD.md                      # Product requirements
├── ARCHITECTURE.md               # This document
├── ARCHITECTURE-ESSENTIALS.md    # Distilled rules for fast context
├── AGENTS.md                     # AI agent operating rules
├── CLAUDE.md                     # CLI quickstart for LLM tools
├── .env.example                  # Example environment variables
├── .gitignore                    # Standard Python ignores
├── database.db                   # SQLite file (created at runtime, gitignored)
├── app/
│   ├── __init__.py
│   ├── config.py                 # Settings via env vars
│   ├── database.py               # Engine, session, init
│   ├── logging_config.py         # Structured logging setup
│   ├── exceptions.py             # Domain exceptions + handlers
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py               # Shared SQLModel base helpers
│   │   └── item.py               # Item table model + DTOs
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── item_create.py
│   │   ├── item_update.py
│   │   └── item_read.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── item_repository.py      # DB-only CRUD, no HTTP awareness
│   ├── services/
│   │   ├── __init__.py
│   │   └── item_service.py        # Business rules on top of repo
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                # FastAPI dependencies (get_session, etc.)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py          # Aggregates v1 routers
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── health.py
│   │           └── items.py
│   └── core/
│       ├── __init__.py
│       └── pagination.py          # skip/limit cursor helpers
└── tests/
    ├── __init__.py
    ├── conftest.py                # Test client + ephemeral SQLite
    ├── test_health.py
    ├── test_items_crud.py
    └── test_items_validation.py
```

## 4. Data Model

### 4.1 Table: `item`

| Column | SQL Type | Nullable | Default | Constraints | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | No | autoincrement | PRIMARY KEY | Surrogate key |
| `name` | TEXT | No | — | NOT NULL, INDEX | Indexed for lookups |
| `description` | TEXT | Yes | NULL | — | Optional |
| `price` | REAL | No | — | NOT NULL, CHECK ≥ 0 | Non-negative enforced in app layer |
| `is_available` | INTEGER (bool) | No | 1 | NOT NULL | SQLite stores bool as 0/1 |

Index: `ix_item_name` on `name`.

### 4.2 SQLModel Definition

```python
# filepath: app/models/item.py
from typing import Optional
from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    name: str = Field(index=True, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    price: float = Field(ge=0.0)
    is_available: bool = True


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    price: Optional[float] = Field(default=None, ge=0.0)
    is_available: Optional[bool] = None


class ItemRead(ItemBase):
    id: int
```

## 5. API Surface (v1)

Base path: `/api/v1`

| Method | Path | Handler | Request Body | Query Params | Response | Status Codes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| GET | `/health` | `health` | — | — | `{"status":"ok"}` | 200 |
| POST | `/api/v1/items/` | `create_item` | `ItemCreate` | — | `ItemRead` | 201, 422 |
| GET | `/api/v1/items/` | `list_items` | — | `skip`, `limit`, `is_available` | `list[ItemRead]` | 200, 422 |
| GET | `/api/v1/items/{item_id}` | `get_item` | — | — | `ItemRead` | 200, 404 |
| PUT | `/api/v1/items/{item_id}` | `replace_item` | `ItemCreate` | — | `ItemRead` | 200, 404, 422 |
| PATCH | `/api/v1/items/{item_id}` | `patch_item` | `ItemUpdate` | — | `ItemRead` | 200, 404, 422 |
| DELETE | `/api/v1/items/{item_id}` | `delete_item` | — | — | — | 204, 404 |

### 5.1 Query Parameter Rules

- `skip`: int ≥ 0, default 0.
- `limit`: int 1..100, default 50.
- `is_available`: optional bool. When provided, filters list to matching rows.

### 5.2 Error Response Shape

All error responses use FastAPI's standard `HTTPException` envelope:

```json
{ "detail": "Item 42 not found" }
```

Validation errors (422) follow FastAPI's default schema with `detail[].loc`, `msg`, `type`.

## 6. Component Responsibilities

| Layer | Responsibility | Forbidden |
| :--- | :--- | :--- |
| `api/v1/endpoints/*` | HTTP shape: parsing, status codes, dependency wiring | DB access, business rules |
| `services/*` | Domain rules: invariants, derived fields, authorization-ready hooks | ORM/SQL knowledge, HTTP types |
| `repositories/*` | Persistence only: pure CRUD on SQLModel entities | HTTP types, business rules |
| `models/*` | Table definitions + DTOs | I/O, logging |
| `core/*` | Cross-cutting helpers (pagination) | App-specific logic |

### 6.1 Dependency Wiring

`get_session()` yields a `sqlmodel.Session` bound to the app's engine. Endpoints accept `session: Session = Depends(get_session)`. Services accept an explicit `session` parameter (no implicit globals). Repositories are stateless module-level functions or classes instantiated per request.

## 7. Database & Engine Configuration

- Engine URL: `sqlite:///./database.db` by default, overridable via `DATABASE_URL` env var.
- `connect_args={"check_same_thread": False}` to permit FastAPI's threadpool.
- `echo` toggled by `SQL_ECHO` env var (default false).
- Tables created via `SQLModel.metadata.create_all(engine)` in the `lifespan` startup hook.
- Foreign keys enabled per connection via `PRAGMA foreign_keys=ON` event listener.

## 8. Application Lifecycle

Use FastAPI's `lifespan` context manager (replaces deprecated `on_event`):

1. **Startup**: configure logging, create engine, run `create_all`, optional seed.
2. **Shutdown**: dispose engine (`engine.dispose()`).

## 9. Configuration

Loaded via `pydantic-settings` (`BaseSettings`):

| Env Var | Default | Description |
| :--- | :--- | :--- |
| `APP_NAME` | `FastAPI + SQLite Persistence API` | OpenAPI title |
| `DATABASE_URL` | `sqlite:///./database.db` | SQLAlchemy URL |
| `SQL_ECHO` | `false` | Echo SQL statements |
| `LOG_LEVEL` | `INFO` | Root log level |
| `CORS_ALLOW_ORIGINS` | `*` | Comma-separated origins for CORS |

Loaded once at import time into `app.config.settings`.

## 10. Logging

- Root logger configured in `app.logging_config`.
- Format: `%(asctime)s | %(levelname)s | %(name)s | %(message)s`.
- Uvicorn loggers reconfigured to use the same format.

## 11. Exception Handling

Custom handlers for:
- `ItemNotFoundError` → `404` with consistent message.
- `ValueError` from services → `422`.
- Unhandled → `500` with generic message (full traceback logged).

## 12. Testing Strategy

| Aspect | Approach |
| :--- | :--- |
| DB isolation | Override `get_session` to use `sqlite:///:memory:` per test. |
| HTTP client | `httpx.AsyncClient` with `ASGITransport(app=app)`. |
| Coverage target | ≥ 90% of `api/`, `services/`, `repositories/`. |
| Markers | `unit`, `integration`. |
| Schema reset | `SQLModel.metadata.drop_all` + `create_all` per fixture. |

## 13. Third-Party Integrations

None required by design. The system is fully self-contained.

## 14. Environment Matrix

| OS | Python | FastAPI | Status |
| :--- | :--- | :--- | :--- |
| Windows 10/11 | 3.10, 3.11, 3.12 | latest | Supported |
| macOS 12+ | 3.10, 3.11, 3.12 | latest | Supported |
| Linux (Ubuntu 22.04+) | 3.10, 3.11, 3.12 | latest | Supported |

## 15. Open Decisions

| ID | Question | Default |
| :--- | :--- | :--- |
| OD-1 | CORS: enable by default? | Yes (permissive for dev). |
| OD-2 | Rate limiting? | No (out of scope per PRD). |
| OD-3 | Background tasks? | No (out of scope per PRD). |

## 16. Migration Path Forward (Future, Not Now)

When the project outgrows SQLite:
1. Swap `DATABASE_URL` to PostgreSQL — SQLModel code unchanged.
2. Introduce Alembic for schema migrations.
3. Introduce a `repositories/` interface + factory so the engine choice is isolated.
4. Add auth middleware (OAuth2 bearer) without touching domain models.