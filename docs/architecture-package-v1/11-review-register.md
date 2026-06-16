# Architecture Package v1.0 — Review Register

## 1. Architectural Review

### Findings

- Clean Architecture is mandatory to prevent UI/database coupling.
- The plugin system must be constrained from day one even if advanced plugins are future releases.
- Event-driven local workflows are appropriate, but audit logs must remain separate.

### Risks

- Developers may place business logic in PySide6 views.
- Plugins may attempt direct database access.
- Module boundaries may blur during rapid development.

### Mitigations

- Enforce dependency rules and PR architecture checklist.
- Provide application service interfaces before UI work.
- Require plugin manifests, ports, and audit wrappers.

### Unresolved Concerns

- Final packaging and installer technology must be selected during implementation planning.

## 2. Scalability Review

### Findings

- SQLite is acceptable for V1 but requires careful write batching and indexing.
- Photo, generated credential, and audit storage will grow continuously because physical deletion is prohibited.
- Batch generation target of 1,000 credentials under 10 minutes requires deterministic rendering and queue management.

### Risks

- SQLite write contention during imports, generation, or printing.
- Disk usage growth from photos and generated artifacts.
- Large audit/report queries impacting UI responsiveness.

### Mitigations

- Use WAL mode, busy timeouts, background workers, indexes, and paginated UI.
- Provide storage diagnostics and backup rotation policies.
- Precompute report snapshots where needed.

### Unresolved Concerns

- Exact hardware baseline for performance targets must be defined before benchmarking.

## 3. Security Review

### Findings

- RBAC, audit, maker-checker, template certification, and credential approval are non-negotiable.
- Offline-only reduces external attack surface but increases reliance on local workstation controls.
- Backup files become highly sensitive data containers.

### Risks

- Shared workstation accounts undermine accountability.
- Local tampering with files or database.
- Unauthorized reprints or approval bypass.
- Backup theft.

### Mitigations

- Require application users, role snapshots, audit hash chains, integrity checks, and permission-level checks.
- Fingerprint assets, templates, photos, generated credentials, and backups.
- Require reprint reasons and optional approval.
- Support backup encryption and restrict backup operations.

### Unresolved Concerns

- Institution-specific authentication policy, password rules, and encryption-at-rest requirements must be finalized.

## 4. Disaster Recovery Review

### Findings

- Backup-before-risky-operations is essential for imports, upgrades, and restore attempts.
- Verified backups and restore drills are as important as backup creation.
- Recovery Center must stage restores before switching active data.

### Risks

- Unverified backups give false confidence.
- Restores overwrite current good data.
- Large asset stores make backup/restore exceed targets.

### Mitigations

- Mandatory verification, emergency backup before restore, staging restore, and periodic recovery tests.
- Backup manifests and hash validation.
- Configurable backup locations and rotation.

### Unresolved Concerns

- External media policy and institutional off-workstation storage process must be defined by deployment owners.

## 5. Maintainability Review

### Findings

- Documentation-first architecture reduces ambiguity before implementation.
- ADRs are required for major technical decisions.
- Configuration-driven rules reduce hardcoded institution logic.

### Risks

- Excessive configurability could create hard-to-test behavior.
- Dynamic fields and policies may become inconsistent.
- Template designer complexity may increase support burden.

### Mitigations

- Schema-validated configuration, policy tests, seeded defaults, and validation reports.
- Version configuration and policies.
- Provide template component library and certification workflow.

### Unresolved Concerns

- Long-term localization strategy should be decided before UI implementation.

## 6. Usability Review

### Findings

- Three modes are required: Quick, Professional, Administrator.
- Quick Mode must simplify steps but cannot bypass approval or security controls.
- Batch workflows need strong validation and item-level feedback.

### Risks

- Users may find Professional/Admin modes too complex.
- Operators may not understand lifecycle states.
- Validation errors during import may be difficult to correct.

### Mitigations

- Mode-based navigation, clear state labels, guided wizards, inline validation, and correction queues.
- Dashboard for pending approvals, expiring credentials, backup status, and print queue health.

### Unresolved Concerns

- Final accessibility and bilingual requirements need stakeholder confirmation.
