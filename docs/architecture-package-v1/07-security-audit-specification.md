# Document 7 — Security & Audit Specification

## 1. Purpose

UICMP security protects identity data, credential issuance, templates, assets, backups, and audit evidence in an offline desktop environment.

## 2. RBAC

Built-in roles:

- Operator
- Reviewer
- Approver
- Printer
- Administrator

Permission model:

```text
permission = module.resource.action.scope
```

Examples:

- `identity.person.create`
- `credential.approval.approve`
- `template.version.certify`
- `printing.job.release`
- `backup.full.create`
- `security.user.manage`

Rules:

- Roles are configurable but built-in roles cannot be physically deleted.
- Administrator can delegate but all delegation is audited.
- Sensitive operations require explicit permissions, not role name checks alone.

## 3. Audit Trail

Audit log requirements:

- Append-only through application behavior.
- Captures actor, role snapshot, action, target, timestamp, workstation, reason, before/after hashes, and correlation ID.
- Security failures are audited.
- Batch operations include batch-level and item-level audit records.

Audited actions include:

- Identity create/update/archive.
- Photo import/process/approve.
- Template validate/certify/publish/archive.
- Credential approve/generate/print/reprint/revoke/archive.
- Import/export.
- Backup/restore.
- User/role/permission changes.
- Diagnostics integrity failures.

## 4. Integrity Verification

Integrity targets:

- Database schema version.
- Sensitive table records.
- Generated PNG/PDF artifacts.
- Template packages.
- Assets.
- Photo originals and processed versions.
- Backup packages.

Verification methods:

- Cryptographic hashes.
- Manifest files.
- Hash chain for audit logs where feasible.
- Scheduled diagnostics.

## 5. Asset Fingerprinting

Asset fingerprint record:

- Asset ID.
- File path.
- Hash algorithm.
- Hash value.
- File size.
- MIME type.
- Created and verified timestamps.

Certified templates include fingerprints of all referenced assets.

## 6. Tamper Detection

Tamper signals:

- Hash mismatch.
- Missing file.
- Unexpected file size change.
- Broken audit chain.
- Modified certified template package.
- Database integrity check failure.

Response:

1. Raise diagnostic finding.
2. Prevent affected production operation.
3. Require administrator review.
4. Record security audit event.
5. Recommend restore from verified backup if needed.

## 7. Approval Workflow

Credential approval stages:

- Draft by Operator.
- Review by Reviewer.
- Approval by Approver.
- Generation after approval.
- Printing by Printer.

Template approval stages:

- Draft by Designer/Administrator.
- Validation.
- Certification.
- Publication.

## 8. Maker-Checker Controls

Maker-checker rules:

- Creator cannot approve their own credential where policy requires maker-checker.
- Template designer cannot certify their own template where policy requires independent certification.
- Reprint may require approval by a different user depending on credential type.
- Administrator emergency override is allowed only if configured and heavily audited.

## 9. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Shared Windows accounts | Require application users and local authentication; log workstation and actor. |
| Privilege creep | Periodic RBAC reports, least privilege defaults, permission-level checks. |
| Audit tampering | Append-only behavior, hash chains, backup inclusion, diagnostics. |
| Unauthorized backup access | Backup encryption option, restricted backup permissions, physical security guidance. |
| Maker-checker bypass | Central approval service and tests; UI cannot approve directly. |
