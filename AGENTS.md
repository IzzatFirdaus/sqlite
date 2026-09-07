# AGENTS.md — Operating Rules for AI Coding Agents

> **Audience:** AI agents (Copilot, Claude, Cursor, Codex, etc.) acting on this repository.
> **Authority hierarchy:** `PRD.md` (what) → `ARCHITECTURE.md` (how) → `ARCHITECTURE-ESSENTIALS.md` (rules at a glance) → this file (how you behave).

---

## 1. Ground Rules

1. **Read first, code second.** Before editing, read `ARCHITECTURE-ESSENTIALS.md` and the relevant module's existing code.
2. **Preserve working code.** Do not rewrite `main.py` or `app/database.py` from scratch unless the task explicitly requires it.
3. **Stay in scope.** Touch only the files needed for the requested change. Never edit `requirements.txt` to add a dependency without an explicit request or PRD approval.
4. **No secrets in source.** Never write API keys, tokens, or credentials to disk. Use `.env` (gitignored) and `pydantic-settings`.
5. **Match existing style.** Type hints on every public function. snake_case modules, PascalCase classes. Line length target 100.
6. **One concern per change.** A refactor + a feature in the same patch is forbidden; split into separate commits.
7. **Never edit generated or runtime artifacts**: `database.db`, `__pycache__/`, `venv/`, `.pytest_cache/`, `*.egg-info/`.

## 2. File Modification Safety

| Path | Risk | Allowed Agent Actions |
|---|---|---|
| `main.py` | High (composition root) | Append router includes; never change lifespan semantics without a task. |
| `app/database.py` | High (engine lifecycle) | Read-only unless task says otherwise. |
| `app/models/*.py` | Medium | Add new entities only when PRD requires them. |
| `app/schemas/*.py` | Low–Medium | Edit freely within the PRD's data model. |
| `app/api/**` | Low | Edit freely; keep imports clean. |
| `app/services/**` | Low | Edit freely; never import from `api/` or `FastAPI`. |
| `app/repositories/**` | Low | Edit freely; never import from `api/` or `services/`. |
| `tests/**` | Low | Add tests with every behavior change. |
| `requirements.txt` | High | Only on explicit request; pin versions. |
| `README.md`, `PRD.md`, `ARCHITECTURE*.md`, `AGENTS.md`, `CLAUDE.md` | Medium | Update to reflect code changes; do not invent features. |
| `.env`, `.env.example` | Low | `.env.example` may be edited; `.env` is read-only context. |

When a file is marked **High** risk, propose the diff in chat before applying it.

## 3. Preferred Design Patterns

- **Composition root in `main.py`**: build the app, configure middleware, include routers.
- **Dependency injection via `Depends`**: `get_session` is the only session source. No globals.
- **Repository + Service separation**: keep persistence concerns in `repositories/`, business rules in `services/`.
- **Pydantic-first validation**: define schemas; never re-validate in route bodies.
- **Lifespan context manager** for startup/shutdown.
- **Structured logging**: every log line includes a module name; no `print()` in app code.
- **Errors as values**: raise typed exceptions from services; map them to HTTP at the API boundary.

## 4. Step-by-Step: Implementing a New Feature

Use this checklist for every feature request:

1. **Read `PRD.md`** and confirm the feature is in scope. If not, stop and ask the user.
2. **Read `ARCHITECTURE-ESSENTIALS.md`** to refresh on layer boundaries.
3. **Locate the target layer**:
   - New entity → add `app/models/<name>.py` and `app/schemas/<name>*.py`.
   - New DB operation → add to `app/repositories/<name>_repository.py`.
   - New business rule → add to `app/services/<name>_service.py`.
   - New HTTP route → add to `app/api/v1/endpoints/<name>.py` and register in `app/api/v1/router.py`.
4. **Wire dependencies**: add to `app/api/deps.py` only if reusable; otherwise inject inline via `Depends`.
5. **Add tests** under `tests/test_<area>.py` covering happy path + at least one failure mode.
6. **Update `README.md`** endpoint table if a new route was added.
7. **Update `ARCHITECTURE.md`** if data model or API surface changed.
8. **Run the verification gate** (Section 6) before declaring done.

## 5. Step-by-Step: Fixing a Bug

1. **Reproduce**: write or identify a failing test that captures the bug.
2. **Locate**: trace from the failing route → service → repository.
3. **Patch** at the lowest layer that fully fixes the issue. Do not paper over at the route layer if the fix belongs in the service.
4. **Re-run tests** including the reproducer.
5. **Add a regression test** if the bug class is non-obvious.

## 6. Verification Gate (run before reporting done)

```powershell
# from project root, venv activated
python -m py_compile main.py
pytest -q
fastapi dev main.py   # manual smoke: curl /health, POST/GET/DELETE /api/v1/items/
```

If any step fails, the task is **not** done. Fix and re-run.

## 7. Forbidden Actions

- Adding auth, rate limiting, websockets, or background tasks without an explicit PRD amendment.
- Switching the ORM, the framework, or the database driver.
- Editing `venv/`, `__pycache__/`, `database.db`.
- Committing `.env` or any file containing a secret.
- Force-pushing or rewriting git history.
- Removing or weakening existing tests to make a build pass.

## 8. Communication Style

- Reply with a short plan (3–7 bullets) before non-trivial edits.
- After edits, summarize what changed and which verification steps were run.
- When uncertain, ask a single clarifying question; do not guess on security or schema-affecting decisions.

## 9. When You Are Stuck

- Re-read `ARCHITECTURE-ESSENTIALS.md`.
- Re-read the failing test or traceback verbatim.
- Search the codebase with `grep_search` or `file_search` before adding new code.
- If still stuck after one attempt, surface the obstacle to the user with the exact error and the options you considered.