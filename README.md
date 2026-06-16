# Universal Identity & Credential Management Platform (UICMP)

This repository currently contains the **Architecture Package v1.0** for UICMP, an enterprise-grade, Windows desktop, offline-only identity and credential lifecycle management platform.

The package is documentation-only by design. It intentionally contains no implementation code, prototypes, or screenshots. The specifications translate the Master Project Specification into implementation-ready guidance for future Python, PySide6, SQLite, SQLAlchemy, Pydantic, ReportLab, OpenCV, Pillow, qrcode, and pytest development.

## Architecture Package v1.0 Deliverables

1. [System Architecture Specification](docs/architecture-package-v1/01-system-architecture-specification.md)
2. [Domain Model Specification](docs/architecture-package-v1/02-domain-model-specification.md)
3. [Database Specification](docs/architecture-package-v1/03-database-specification.md)
4. [Template Engine Specification](docs/architecture-package-v1/04-template-engine-specification.md)
5. [Printing Engine Specification](docs/architecture-package-v1/05-printing-engine-specification.md)
6. [Photo Intelligence Specification](docs/architecture-package-v1/06-photo-intelligence-specification.md)
7. [Security & Audit Specification](docs/architecture-package-v1/07-security-audit-specification.md)
8. [Backup & Recovery Specification](docs/architecture-package-v1/08-backup-recovery-specification.md)
9. [UI/UX Blueprint](docs/architecture-package-v1/09-ui-ux-blueprint.md)
10. [Development Standards Specification](docs/architecture-package-v1/10-development-standards-specification.md)
11. [Architecture Review Register](docs/architecture-package-v1/11-review-register.md)

## Non-Negotiable Product Constraints

- Offline only; no cloud services, internet dependency, online verification, or telemetry.
- Windows desktop application built with Python and PySide6.
- SQLite for V1, with repository and unit-of-work boundaries that allow future PostgreSQL or SQL Server migration.
- Clean Architecture with no business logic in the UI and no direct database access from presentation code.
- No physical delete; archive, revoke, expire, and supersede records instead.
- Everything versioned, auditable, configuration driven, and designed for plugin expansion.
- Template certification and credential approval are mandatory production gates.
