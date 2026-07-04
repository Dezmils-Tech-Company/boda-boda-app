# Copilot instructions

This repository is a FastAPI backend for a Flutter mobile application. Prioritize robust, production-ready API behavior over scaffolding.

## What to optimize for
- Build real backend features with durable validation, clear auth, and reliable persistence.
- Avoid placeholder implementations, fake data, and deferred logic.
- Keep the API consistent with the existing router/service/repository/model structure.

## Architecture guidance
- Use the existing layered structure in [app/main.py](../app/main.py), [app/routers](../app/routers), [app/services](../app/services), [app/repositories](../app/repositories), [app/models](../app/models), and [app/schemas](../app/schemas).
- Keep route handlers thin and let services own business rules.
- Use Beanie/Motor and async database access patterns already established in [app/core/database.py](../app/core/database.py).
- Read configuration from [app/core/config.py](../app/core/config.py) and reuse the shared auth helpers in [app/core/security.py](../app/core/security.py).

## Backend standards
- Validate every external input with Pydantic schemas.
- Return meaningful HTTP errors instead of silently accepting invalid states.
- Enforce authorization checks for protected endpoints.
- Prefer end-to-end implementations over partial stubs.
- Keep response payloads simple and predictable for mobile clients.

## Development commands
- Start the API locally: python run.py
- Run tests: pytest
- Quick syntax check: python -m compileall app
