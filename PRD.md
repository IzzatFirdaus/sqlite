# Product Requirements Document (PRD)

> **Project:** SQLite + FastAPI Persistence API
> **Status:** Draft v1.0
> **Scope:** Lightweight CRUD service demonstrating persistent storage with FastAPI and SQLite.

---

## 1. Product Overview

A self-contained RESTful API that exposes create, read, list, update, and delete operations for a catalog resource ("Item"), backed by a persistent SQLite database file. The product is positioned as a **reference implementation / starter template** for developers learning FastAPI + SQLModel, and as a minimal backend suitable for local prototyping.

The product deliberately avoids premature enterprise features (auth, multi-tenancy, queues, microservices) so the surface area remains small, learnable, and self-contained in a single Python file.

## 2. Goals & Non-Goals

### 2.1 Goals
- Demonstrate idiomatic FastAPI + SQLModel + SQLite integration in one minimal, runnable service.
- Provide a persistent CRUD surface for a single `Item` resource.
- Ship interactive API documentation (OpenAPI/Swagger UI) out of the box.
- Make setup trivial: a single `pip install` and one command to run.
- Be a reliable starting point that can be safely extended.

### 2.2 Non-Goals (out of scope)
- Authentication, authorization, sessions, or user accounts.
- Multi-user concurrency guarantees beyond what SQLite provides.
- File uploads, background jobs, websockets, or streaming.
- Production deployment hardening (TLS termination, reverse proxy, container orchestration).
- Distributed or networked database usage.

## 3. Target Audience & Personas

| Persona | Description | Primary Need |
| :--- | :--- | :--- |
| **Learner Developer** | Engineer new to FastAPI/SQLModel who wants a working reference. | A minimal, well-documented example they can read end-to-end. |
| **Prototype Builder** | Developer spinning up a quick backend for a hackathon or spike. | Fast iteration and zero-config local persistence. |
| **Workshop Instructor** | Teacher running a FastAPI tutorial. | A clean baseline that students can extend. |
| **Reviewer / Interviewer** | Technical evaluator inspecting code quality. | Idiomatic patterns and a coherent small scope. |

## 4. Functional Requirements

| ID | Requirement | Priority |
| :--- | :--- | :--- |
| FR-1 | The system shall expose a `POST /items/` endpoint that creates a new `Item` record and returns it with the assigned `id`. | Must |
| FR-2 | The system shall expose a `GET /items/` endpoint that returns the full list of `Item` records. | Must |
| FR-3 | The system shall expose a `GET /items/{item_id}` endpoint that returns a single `Item` or `404` if absent. | Must |
| FR-4 | The system shall expose a `PUT /items/{item_id}` endpoint that fully replaces an `Item` or returns `404`. | Must |
| FR-5 | The system shall expose a `PATCH /items/{item_id}` endpoint that partially updates an `Item` or returns `404`. | Must |
| FR-6 | The system shall expose a `DELETE /items/{item_id}` endpoint that removes an `Item` or returns `404`. | Must |
| FR-7 | The system shall persist data across server restarts in a local SQLite file. | Must |
| FR-8 | The system shall automatically create database tables on startup if they do not exist. | Must |
| FR-9 | The system shall validate all inbound payloads via Pydantic/SQLModel and reject malformed input with `422`. | Must |
| FR-10 | The system shall provide OpenAPI documentation at `/docs` and a JSON schema at `/openapi.json`. | Must |
| FR-11 | The system shall support basic search/filter on list endpoints (e.g., by availability). | Should |
| FR-12 | The system shall support pagination on the list endpoint (limit + offset). | Should |
| FR-13 | The system shall return clear, structured error responses for all failure cases. | Must |

## 5. Non-Functional Requirements

| ID | Category | Requirement |
| :--- | :--- | :--- |
| NFR-1 | Performance | Single-process latency under 50 ms for any endpoint with < 10k rows. |
| NFR-2 | Reliability | Data survives process restart; no partial writes on crash. |
| NFR-3 | Maintainability | All route logic isolated from persistence; schema changes require single-file edits. |
| NFR-4 | Observability | Structured logging of requests and errors; `/health` endpoint for liveness. |
| NFR-5 | Portability | Runs on Python 3.10+ on Windows, macOS, and Linux without platform-specific code. |
| NFR-6 | Testability | Pure dependency-injected session; unit tests run with an in-memory SQLite. |
| NFR-7 | Security | No secrets in source; input validated at the API boundary; no SQL string concatenation. |
| NFR-8 | Documentation | Every public endpoint documented in OpenAPI with example payloads. |

## 6. Domain Model (Product View)

**Resource: Item**
- Represents a catalog entry (think product, task, or note — the model is intentionally generic).
- Attributes:
  - `id` — surrogate primary key.
  - `name` — human-readable label.
  - `description` — optional longer text.
  - `price` — non-negative numeric value.
  - `is_available` — boolean flag.

## 7. Key User Flows

### 7.1 Create Item
1. Client sends `POST /items/` with a JSON body matching the `Item` schema (without `id`).
2. Server validates input, inserts row, returns `201 Created` with the persisted object including `id`.
3. On validation failure, server returns `422` with a field-level error list.

### 7.2 List Items
1. Client sends `GET /items/` with optional `skip`, `limit`, `is_available` filters.
2. Server returns `200 OK` with an array (possibly empty).
3. Out-of-range paging returns an empty array (not an error).

### 7.3 Read Item
1. Client sends `GET /items/{item_id}`.
2. If the item exists, server returns `200 OK` with the item.
3. Otherwise, server returns `404 Not Found` with a structured error body.

### 7.4 Update Item
1. Client sends `PUT /items/{item_id}` (full body) or `PATCH /items/{item_id}` (partial).
2. Server validates input, updates the row, returns `200 OK` with the updated object.
3. If the item does not exist, server returns `404 Not Found`.

### 7.5 Delete Item
1. Client sends `DELETE /items/{item_id}`.
2. If the item exists, server removes it and returns `204 No Content`.
3. Otherwise, server returns `404 Not Found`.

### 7.6 Health Check
1. Client sends `GET /health`.
2. Server returns `200 OK` with `{"status": "ok"}` if the process and DB are responsive.

## 8. Edge Cases & Error Behaviors

| Scenario | Expected Behavior |
| :--- | :--- |
| Item not found by ID | `404` with `{"detail": "Item <id> not found"}` |
| Negative or non-numeric `price` | `422` with field error |
| Missing required `name` | `422` with field error |
| `id` provided by client on create | Ignored (server-assigned) |
| Concurrent writes to same row | Last write wins; SQLite serializes within process |
| DB file missing | Recreated automatically on startup |
| Invalid query parameter type | `422` with parameter error |
| Empty list result | `200 OK` with `[]` |
| Idempotent delete | `404` on second delete of same id |

## 9. Success Metrics

| Metric | Target |
| :--- | :--- |
| Time-to-first-successful-request for a new dev | < 5 minutes from clone |
| OpenAPI spec completeness | 100% of routes documented |
| Test coverage of route handlers | ≥ 90% |
| Crash-free startup across supported Python versions | 100% |
| Docs page reachable on `127.0.0.1:8000/docs` | 100% |

## 10. Release Criteria

- All "Must" functional requirements implemented and verified.
- `/health` returns 200.
- All routes return expected status codes per the flow matrix.
- Documentation updated to reflect actual endpoints.
- Dependencies pinned in `requirements.txt`.