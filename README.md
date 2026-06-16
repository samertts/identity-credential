# Universal Identity & Credential Management Platform (UICMP)

UICMP is a professional offline-only Windows desktop platform for identity and credential lifecycle management. It is designed for government institutions, healthcare organizations, universities, private companies, and other entities that require audited, versioned, certification-driven credential operations without cloud or internet dependencies.

## V1 Architecture Baseline

The repository is organized around Clean Modular Architecture:

- `src/uicmp/presentation`: PySide6 desktop UI and view models only.
- `src/uicmp/application`: service layer, workflows, validation orchestration, and ports.
- `src/uicmp/domain`: framework-independent entities, lifecycle states, and policies.
- `src/uicmp/infrastructure`: adapters for offline resources, image/PDF/QR/printing, backups, diagnostics, and plugins.
- `src/uicmp/data`: SQLAlchemy persistence adapters for SQLite V1, with a future migration path to PostgreSQL or SQL Server.
- `src/uicmp/plugins`: extension points for future RFID, NFC, digital identity, OCR, and access-control integrations.

## Core Invariants

1. Offline only: no internet, cloud, or network service dependency.
2. No physical delete: records are archived and versioned.
3. Everything audited: lifecycle-changing service operations emit audit events.
4. Certification required: production credential generation requires a certified template version.
5. UI isolation: presentation code must call application services and must not access the database directly.
6. Plugin ready: future integrations must use ports/adapters and avoid core redesign.

## Development

```bash
pytest -q
python -m compileall -q src tests
```

The `pyproject.toml` declares the target production stack: Python, PySide6, SQLAlchemy, Pydantic, ReportLab, OpenCV, Pillow, qrcode, and pytest.
