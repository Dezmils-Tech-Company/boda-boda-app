# AGENTS.md

This repository is a FastAPI backend for a Flutter mobile application. Treat it as a production service, not a prototype. Implement real behavior, validate inputs, and avoid placeholder logic.

## Project context
- Primary app entrypoint: [app/main.py](app/main.py)
- Configuration and environment loading: [app/core/config.py](app/core/config.py)
- Database initialization with Beanie/Motor: [app/core/database.py](app/core/database.py)
- API routes live under [app/routers](app/routers)
- Business logic belongs in [app/services](app/services)
- Persistence logic belongs in [app/repositories](app/repositories)
- Schemas and validation live in [app/schemas](app/schemas)
- Data models live in [app/models](app/models)

Reference [README.md](README.md) and [app/README.md](app/README.md) for broader project context, but keep instructions here focused and actionable.

## Working rules for agents
- Build a robust backend for the Flutter app: clear contracts, stable response shapes, strong validation, and sensible error handling.
- Do not add placeholder logic, fake success paths, TODOs, or “to be done later” behavior. If a requirement is unclear, ask for clarification rather than inventing incomplete behavior.
- Prefer real implementations over stubs. Any new feature must be wired end-to-end through router, service, schema, and model layers as appropriate.
- Keep business logic in services and repositories; routers should stay thin and focused on HTTP concerns.
- Use FastAPI dependency injection and Pydantic schemas consistently.
- Handle failures with explicit HTTP exceptions and clear messages.
- Keep API routes versioned under /api/v1/ and use meaningful resource names.
- Ensure responses are mobile-friendly: predictable JSON, minimal nesting where possible, and clear field names.

## Architecture conventions
- Follow the existing layering:
  - routers: request/response handling and dependency injection
  - services: business rules and orchestration
  - repositories: database access helpers
  - models: Beanie documents
  - schemas: request/response validation and serialization
- Keep database access async and use Beanie/Motor patterns already present in the project.
- Use the shared settings object from [app/core/config.py](app/core/config.py) instead of introducing ad-hoc environment handling.
- Reuse existing auth and permission helpers from [app/core/security.py](app/core/security.py) and [app/core/permissions.py](app/core/permissions.py).

## Implementation expectations
- Validate request bodies and query parameters with Pydantic.
- Add or update schemas when changing request or response payloads.
- Ensure authentication, authorization, and user role checks are enforced where appropriate.
- Avoid hard-coded secrets; rely on environment configuration.
- If a change affects API behavior, update the corresponding router/service/schema flow rather than patching around it.
- When adding features, include real persistence and real error handling, not mock data.

## Quality bar
- Prefer correctness and reliability over quick shortcuts.
- Preserve existing conventions unless a change clearly improves the architecture.
- Prefer small, focused changes that fit the current structure.
- If a feature cannot be implemented safely without guessing, stop and request clarification.

## Commands
- Start the backend locally: python run.py
- Run tests: pytest
- Check syntax quickly: python -m compileall app
