# Architecture Essentials

> **Purpose:** High-signal, low-volume reference. Load this first; reach for `ARCHITECTURE.md` only when details are needed.

---

## 1. Non-Negotiable Rules

1. **Layered architecture is mandatory.**
   `api → services → repositories → models`. No skipping layers; no upward imports.
2. **HTTP types stay out of services and repositories.** No `HTTPException` below `api/`.
3. **All endpoints depend on `get_session()`** via FastAPI `Depends`. No module-level sessions.
4. **Use the `lifespan` context manager** for startup/shutdown. Do not use `@app.on_event`.
5. **Configuration via `pydantic-settings`** in `app/config.py`. No hardcoded URLs or secrets.
6. **Validation lives in Pydantic/SQLModel**, not in hand-rolled `if` chains.
8. **Tables are created on startup** via `SQLModel.metadata.create_all(engine)`. No Alembic yet.
9. **Errors use `HTTPException`** with `detail` strings; services raise domain exceptions, never HTTP types.
10. **No business logic in route handlers.** Routes parse, call services, format responses.

## 2. Core Data Structures

### 2.1 `Item` table model

| Field | Type | Constraints |
| :--- | :--- | :--- |
| `id` | `int?` | PK, autoincrement |
| `name` | `str` | required, indexed, 1..200 chars |
| `description` | `str?` | optional, ≤ 2000 chars |
| `price` | `float` | required, ≥ 0 |
| `is_available` | `bool` | default `True` |

### 2.2 DTOs (under `app/schemas/`)

- `ItemCreate` — required `name`, `price`; optional `description`; default `is_available=True`.
- `ItemUpdate` — every field optional; `None` means "do not change".
- `ItemRead` — `Item` fields plus always-present `id: int`.

### 2.3 Pagination

- `skip: int = 0`, `limit: int = 50` (clamped 1..100).
- `is_available: bool | None` filter supported on list endpoint.

## 3. Primary Routes (v1, base `/api/v1`)

| Method | Path | Purpose |
| :--- | :--- | :--- |
| GET | `/health` | Liveness probe |
| POST | `/items/` | Create item (201) |
| GET | `/items/` | List with `skip`, `limit`, `is_available` |
| GET | `/items/{item_id}` | Read one (404 if missing) |
| PUT | `/items/{item_id}` | Full replace (404 if missing) |
| PATCH | `/items/{item_id}` | Partial update (404 if missing) |
| DELETE | `/items/{item_id}` | Delete (204 on success, 404 if missing) |

## 4. Module Map (one-line per file)

| File | Owns |
| :--- | :--- |
| `main.py` | FastAPI app factory, router include, lifespan |
| `app/config.py` | Settings via env |
| `app/database.py` | Engine, `get_session`, `create_db_and_tables` |
| `app/logging_config.py` | Log format & level |
| `app/exceptions.py` | `ItemNotFoundError`, handlers |
| `app/models/item.py` | `Item` table model + `ItemBase` |
| `app/schemas/item_*.py` | `ItemCreate` / `ItemUpdate` / `ItemRead` |
| `app/repositories/item_repository.py` | DB-only CRUD on `Item` |
| `app/services/item_service.py` | Business rules, raises `ItemNotFoundError` |
| `app/api/v1/endpoints/items.py` | HTTP routes for items |
| `app/api/v1/endpoints/health.py` | `/health` |
| `app/api/v1/router.py` | Aggregates endpoints |
| `app/api/deps.py` | Reusable dependencies |
| `app/core/pagination.py` | `skip`, `limit` clamping |
| `tests/*` | pytest suite, in-memory SQLite |

## 5. Environment Variables

| Name | Default |
| :--- | :--- |
| `DATABASE_URL` | `sqlite:///./database.db` |
| `SQL_ECHO` | `false` |
| `LOG_LEVEL` | `INFO` |
| `APP_NAME` | `FastAPI + SQLite Persistence API` |
| `CORS_ALLOW_ORIGINS` | `*` |

## 6. Quick Commands

- Install: `pip install -r requirements.txt`
- Run dev: `fastapi dev main.py`
- Run prod: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Test: `pytest -q`
- Lint: `ruff check .`
- Format: `ruff format .`

---

## 7. Critical Stress-Test Self-Audit

### What will break first under load or edge cases?
- **Concurrent writes**: SQLite serializes writes; under high write throughput from multiple threads, requests will queue. Read-heavy workloads are fine, write-heavy are not.
- **Single-file DB contention**: All endpoints share one `database.db`; WAL mode is not configured by default. A burst of concurrent updates will produce `OperationalError: database is locked` without PRAGMA tuning.
- **Large `list_items` results**: No pagination is enforced server-side beyond `limit`; deep `skip` paging is O(n) in SQLite.
- **Float `price`**: Monetary values in `float` lose precision. Once real money enters, switch to `Decimal`.

### What failure modes or edge cases are currently unaccounted for?
- **No retry / idempotency on `POST`**: A client retry of a network failure can create duplicates (no `Idempotency-Key`).
- **No graceful shutdown of in-flight requests**: `engine.dispose()` runs immediately; any open session is severed.
- **No request ID / correlation**: Failures are hard to trace across logs.
- **Pydantic v2 + SQLModel edge cases**: `Optional[str]` fields accept `None` even when the column is `NOT NULL` if validation is bypassed via `model_validate`; needs explicit guards at the service.
- **PATCH semantics ambiguity**: `null` vs missing field is indistinguishable in JSON; the spec treats both as "no change" but does not document it.

### Which parts of this design are over-engineered and can be simplified?
- **The `repositories/` + `services/` split** is over-engineered for a single-table CRUD demo. For the current scope, a thin service that talks to the ORM directly is sufficient; the repository layer can be introduced later when a second entity appears.
- **`core/pagination.py`** is a one-line clamp; an inlined `Query(0, ge=0)` parameter set would suffice.
- **Custom exception handlers** for a single `ItemNotFoundError` are not strictly needed; `HTTPException` raised from services mapped through one helper is enough for v1.
- **Env-driven CORS origins parsing** adds complexity that only matters once a frontend exists; default permissive CORS for now is fine.