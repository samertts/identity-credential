# Document 1 — System Architecture Specification

## 1. Purpose

The Universal Identity & Credential Management Platform (UICMP) is a Windows desktop, offline-only identity and credential lifecycle platform. It manages persons, organizations, departments, memberships, photos, templates, credential issuance, approval, generation, printing, reports, diagnostics, backups, recovery, and future plugins without internet or cloud dependency.

## 2. Architectural Drivers

| Driver | Architectural Response |
|---|---|
| Offline only | All services use local adapters only. Network calls are prohibited by dependency policy, code review, and tests. |
| Long-term institutional use | Stable domain model, versioned records, migration-ready persistence, documented extension points. |
| Security before convenience | RBAC, maker-checker, audit trail, integrity verification, certification gates. |
| No physical delete | Archival flags, status transitions, superseded versions, immutable audit events. |
| Configuration driven | Policies, credential types, templates, printer profiles, rules, and UI modes are stored as versioned configuration. |
| Plugin ready | Plugins integrate through explicit ports and local manifests; plugins cannot bypass core security and audit services. |

## 3. Layer Diagram

```text
+-------------------------------------------------------------+
| Presentation Layer                                           |
| PySide6 screens, dialogs, view models, command dispatch      |
+---------------------------|---------------------------------+
                            v
+-------------------------------------------------------------+
| Application Layer                                            |
| Use cases, services, workflows, validation orchestration,    |
| authorization checks, transactions, events                   |
+---------------------------|---------------------------------+
                            v
+-------------------------------------------------------------+
| Domain Layer                                                 |
| Entities, aggregates, value objects, policies, lifecycle     |
| rules, domain events                                         |
+---------------------------|---------------------------------+
                            v
+-------------------------------------------------------------+
| Infrastructure Layer                                         |
| PDF/PNG generation, QR, image processing, camera, printing,  |
| import/export, backup, diagnostics, plugin loading           |
+---------------------------|---------------------------------+
                            v
+-------------------------------------------------------------+
| Data Layer                                                   |
| SQLAlchemy repositories, unit of work, migrations, SQLite    |
+-------------------------------------------------------------+
```

Dependency direction is inward. Presentation depends on Application interfaces; Application depends on Domain and ports; Infrastructure and Data implement ports. Domain depends on no other platform layer.

## 4. Module Diagram

```text
UICMP
├── Identity Management
├── Membership & Organization Management
├── Credential Lifecycle
├── Template Engine
├── Photo Intelligence
├── QR/Barcode Engine
├── Generation Engine
├── Printing Engine
├── Import Engine
├── Export Engine
├── Reporting
├── Diagnostics / Health Monitor
├── Backup & Recovery
├── Security / RBAC / Audit
├── Rules Engine
├── Event System
└── Plugin Host
```

Each module exposes application services and receives dependencies through ports. Cross-module communication uses application services and domain/application events, not direct table access.

## 5. Service Diagram

```text
UI Command
  -> AuthorizationService
  -> Use Case Service
  -> ValidationService
  -> Repository / UnitOfWork
  -> EventPublisher
  -> AuditService
  -> NotificationCenter (local UI only)
```

Required application services:

- `IdentityService`
- `MembershipService`
- `PhotoService`
- `TemplateService`
- `TemplateCertificationService`
- `CredentialService`
- `CredentialApprovalService`
- `CredentialGenerationService`
- `PrintQueueService`
- `ImportService`
- `ExportService`
- `BackupService`
- `RecoveryService`
- `ReportService`
- `DiagnosticsService`
- `RulesEvaluationService`
- `PluginRegistryService`
- `AuditService`
- `AuthorizationService`

## 6. Event Architecture

UICMP uses an in-process event bus backed by a durable local event log. Events are emitted after successful unit-of-work commits. Events are not a substitute for audit logs; events describe system facts while audit logs describe accountable user/system actions.

Mandatory event categories:

- Identity: `PersonCreated`, `PersonUpdated`, `OrganizationCreated`, `DepartmentCreated`, `MembershipChanged`
- Photo: `PhotoImported`, `PhotoProcessed`, `PhotoQualityEvaluated`
- Template: `TemplateVersionCreated`, `TemplateValidated`, `TemplateCertified`, `TemplatePublished`
- Credential: `CredentialDrafted`, `CredentialSubmittedForReview`, `CredentialApproved`, `CredentialGenerated`, `CredentialPrinted`, `CredentialRevoked`, `CredentialArchived`
- Import/Export: `ImportValidated`, `ImportCompleted`, `ExportCompleted`
- Backup/Recovery: `BackupCreated`, `BackupVerified`, `RestoreCompleted`
- Security: `LoginSucceeded`, `LoginFailed`, `PermissionDenied`, `IntegrityCheckFailed`

Event delivery rules:

1. Events are persisted locally before asynchronous handlers run.
2. Handlers must be idempotent.
3. Handler failures are retried locally and surfaced in diagnostics.
4. No event handler may perform network I/O.

## 7. Plugin Architecture

Plugins are future-facing but the host architecture is present from V1.

Plugin package contents:

```text
plugin-package.zip
├── manifest.json
├── plugin.py
├── resources/
├── migrations/       # optional, reviewed before install
└── signatures/       # optional V1, mandatory later
```

Manifest fields:

- `plugin_id`
- `name`
- `version`
- `vendor`
- `supported_uicmp_versions`
- `capabilities`
- `required_permissions`
- `entry_points`
- `configuration_schema`
- `integrity_hashes`

Plugin rules:

1. Plugins are local-only and installed by administrators.
2. Plugins cannot access database sessions directly.
3. Plugins use declared ports and are subject to RBAC and audit.
4. Plugins cannot override credential approval, audit, backup, or certification gates.
5. Plugin failures are isolated and reported through diagnostics.

## 8. Dependency Rules

- UI must not import SQLAlchemy models or database sessions.
- Domain must not import PySide6, SQLAlchemy, ReportLab, OpenCV, Pillow, or qrcode.
- Application services may depend on domain objects and abstract ports.
- Infrastructure adapters implement ports and may depend on external libraries.
- Data adapters implement repository ports and own database mapping concerns.
- Cross-module writes occur through application services only.

## 9. Data Flow

### 9.1 Issue Credential Flow

```text
Operator selects entity
 -> Application validates identity and credential type
 -> Rules engine resolves expiry/template defaults
 -> Draft credential is created
 -> Audit event recorded
 -> Reviewer reviews
 -> Approver approves (maker-checker enforced)
 -> Generation service verifies certified template
 -> PNG/PDF generated locally
 -> Print queue item created
 -> Printer prints
 -> Print history recorded
```

### 9.2 Import Flow

```text
User selects file/folder
 -> Import wizard profiles source
 -> Validation runs without committing
 -> User reviews errors and mapping
 -> Backup prompt for risky batch operations
 -> Batch import transaction executes
 -> Photos matched and queued for processing
 -> Import report and audit logs written
```

## 10. Error Handling Strategy

Errors are classified as:

- Validation errors: user-correctable input problems.
- Authorization errors: permission or maker-checker violations.
- Integrity errors: hash mismatch, tamper signal, corrupt package.
- Operational errors: printer unavailable, disk space low, camera unavailable.
- System errors: unexpected exceptions requiring diagnostics capture.

Rules:

1. Do not expose stack traces to ordinary users.
2. Preserve technical diagnostics locally for administrators.
3. All failed security-sensitive operations are audited.
4. Batch operations produce item-level error reports.
5. Risky operations require backup confirmation when configured.

## 11. Upgrade Strategy

V1 uses SQLite with SQLAlchemy migrations. Future database migration is protected by repository interfaces, service-layer transactions, and schema version records.

Upgrade process:

1. Verify current backup.
2. Create migration backup.
3. Verify disk space and database integrity.
4. Apply migrations in order.
5. Recompute integrity metadata where required.
6. Run post-upgrade diagnostics.
7. Record upgrade audit event.

Rollback requires restoring the migration backup; destructive downgrade scripts are prohibited.

## 12. Key Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| SQLite contention during batch work | Slow writes or locked database | Use unit-of-work batching, WAL mode, busy timeout, background queues, and clear progress UI. |
| Plugin bypass of core rules | Security failure | Ports only, manifest permissions, plugin sandbox policy, audit wrapping, administrator-only install. |
| UI business logic creep | Maintainability loss | Enforce import rules, code review checklist, service-only UI commands. |
| Event handler failure | Incomplete side effects | Durable local event log, retry queue, diagnostics surfacing. |
| Upgrade corruption | Operational outage | Mandatory migration backup and post-upgrade verification. |
