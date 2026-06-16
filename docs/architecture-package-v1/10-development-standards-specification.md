# Document 10 — Development Standards Specification

## 1. Purpose

This document defines implementation standards for future development. The current Architecture Package v1.0 is documentation-only and intentionally contains no application code.

## 2. Folder Structure

Future code should use:

```text
src/uicmp/
├── presentation/
├── application/
├── domain/
├── infrastructure/
├── data/
├── plugins/
└── shared/

tests/
├── unit/
├── integration/
├── ui/
├── performance/
└── disaster_recovery/

docs/
├── architecture-package-v1/
└── adr/
```

## 3. Naming Standards

- Python packages: lowercase with underscores where needed.
- Classes: `PascalCase`.
- Functions and variables: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Database tables: plural `snake_case`.
- Domain events: past-tense `PascalCase` such as `CredentialApproved`.
- Permissions: dotted lowercase such as `credential.approval.approve`.

## 4. Coding Standards

- No business logic in UI classes.
- No direct database access from UI.
- No network dependency for core features.
- Never physically delete business records through application behavior.
- Use services/use cases for lifecycle transitions.
- Use Pydantic schemas for validation boundaries.
- Use SQLAlchemy repositories and unit-of-work for persistence.
- Record audit logs for sensitive operations.
- Write deterministic rendering and generation code.
- Do not put try/catch blocks around imports.

## 5. Git Strategy

- Main branch contains releasable documentation/code.
- Feature branches are short-lived.
- Pull requests require review for architecture, security, tests, and offline compliance.
- Architectural changes require ADRs.
- Migration changes require rollback/restore notes.

## 6. Branch Strategy

Recommended branches:

- `main`
- `feature/<area>-<short-description>`
- `fix/<area>-<short-description>`
- `docs/<short-description>`
- `release/vX.Y.Z`

## 7. Testing Strategy

Targets:

- Unit coverage target: 90%+.
- Application service tests for all lifecycle rules.
- Repository integration tests using SQLite.
- Template validation tests.
- Credential validation tests.
- Backup validation and restore tests.
- Stress tests for 1,000 credential batch generation under target time.
- Security tests for RBAC, maker-checker, and audit.
- Offline compliance tests ensuring no network calls.

## 8. Release Strategy

Release process:

1. Freeze features.
2. Run full test suite.
3. Run performance and stress tests.
4. Run disaster recovery tests.
5. Verify documentation and migration notes.
6. Create release backup/restore validation package.
7. Sign or fingerprint release artifacts where possible.
8. Publish offline installer/package internally.

## 9. Architecture Decision Records

ADRs are required for:

- Database migration strategy changes.
- Security model changes.
- Plugin capability expansion.
- Rendering engine changes.
- Backup format changes.
- Any exception to offline-only behavior.

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Standards ignored under schedule pressure | PR checklist and release gates. |
| Tests become slow and skipped | Layered test pyramid and dedicated stress suite. |
| Inconsistent architecture across modules | ADRs, code owners, dependency checks. |
| Offline rule accidentally violated | Static checks, dependency review, integration tests blocking network calls. |
| Database migrations unsafe | Mandatory migration backup, tests, and restore drills. |
