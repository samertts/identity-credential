# UICMP V1 Architecture Baseline

UICMP is an offline-only Windows desktop identity and credential lifecycle platform.
The initial codebase is organized around Clean Modular Architecture:

- `presentation`: PySide6 desktop UI and view models only.
- `application`: service layer, workflows, validation orchestration, and ports.
- `domain`: framework-independent entities, value objects, lifecycle states, and policies.
- `infrastructure`: adapters for files, image processing, PDF/PNG generation, QR, printing, backups, diagnostics, and plugins.
- `data`: SQLAlchemy persistence adapters targeting SQLite V1 with a future migration path to PostgreSQL or SQL Server.

Core invariants:

1. Offline-only operation; network endpoints are rejected by infrastructure policy.
2. No physical delete; records are archived and versioned.
3. Template and credential certification gates are enforced before production generation.
4. UI code must call application services and must not access the database directly.
5. All lifecycle-changing operations must emit audit events.
6. Plugins integrate through ports/adapters and must not require core redesign.
