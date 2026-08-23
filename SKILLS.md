---
name: apcafeteria-backend
description: Build and maintain the APCafeteria Flask backend, database schema, migrations, seeders, and portal APIs while preserving its layered architecture.
---

# APCafeteria Backend

Use this project guide for changes inside `apcafeteria-backend`.

## Architecture invariants

- Keep routes registration-only and group all endpoints for a portal in its corresponding route file.
- Keep controllers limited to HTTP input/output concerns: validate input, call a service, and format the response.
- Put request and parameter validation in `validations`; report field errors with `ValidationError`.
- Put workflows, calculations, transactions, and integrations in `services`. Services must not access Flask request or response objects.
- Keep one SQLAlchemy table model per file in `models`, including every persisted column.
- Keep CORS, rate limiting, and JWT checks as separate modules in `middlewares`.
- Keep JWT, response, password hashing, and logging utilities as separate modules in `helpers`.

## Database synchronization

For every schema change, update all four representations in the same change:

1. the relevant one-table model;
2. a focused Alembic revision under `database/migrations/versions`;
3. `database/schema.sql`;
4. `database/erd/apcafeteria.mmd`.

Do not edit an already-applied migration to represent a later change. Add a new revision. Preserve foreign-key dependency order in upgrades and reverse it in downgrades.

## Security and verification

- Never expose user or shop password hashes in responses or logs.
- Validate all client-controlled values before a service uses them.
- Require JWT roles at the route boundary for restricted portals.
- Keep secrets only in `.env`; add safe placeholders to `.env.example`.
- Run `pytest`, import every model, and run `alembic upgrade head --sql` before handing off database changes.
- Prefer `python manage.py` as the unified entry point for migrations, seeders, tests, and the development server.
