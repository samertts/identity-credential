# Document 8 — Backup & Recovery Specification

## 1. Purpose

Backup and Recovery protects UICMP institutions from data loss, corruption, failed upgrades, operator error, and disaster scenarios while remaining fully offline.

## 2. Backup Types

### Quick Backup

Includes database only and critical metadata. Used before moderate-risk operations.

### Full Backup

Includes:

- Database.
- Photos.
- Templates.
- Assets.
- Generated credentials.
- Reports.
- Audit logs.
- Configuration.
- Plugin packages and manifests.
- Backup manifest and hashes.

### Migration Backup

Mandatory before schema/application upgrades. Full fidelity and clearly labeled with source application/schema version.

### Emergency Backup

Administrator-triggered backup during diagnostics or before recovery operations.

## 3. Backup Rotation

Configurable default:

- Daily backups retained for 30 days.
- Monthly backups retained for 12 months.
- Yearly backups retained for 7 years or institution policy.

Rotation never deletes backup records without audit. Physical cleanup of backup files requires administrator permission and institutional policy confirmation.

## 4. Backup Verification

Verification steps:

1. Confirm manifest completeness.
2. Verify database integrity.
3. Verify file hashes.
4. Verify schema version metadata.
5. Verify minimum restore prerequisites.
6. Record verification result.

Unverified backups cannot be marked recovery-ready.

## 5. Restore Process

```text
Administrator opens Recovery Center
 -> Select backup
 -> System verifies backup
 -> Current system emergency backup is offered/required by policy
 -> Restore plan displayed
 -> Restore executes to staging location
 -> Integrity validation runs
 -> System switches active data directory
 -> Post-restore diagnostics run
 -> Restore audit record written
```

## 6. Disaster Recovery

Disaster scenarios:

- Database corruption.
- Asset/photo loss.
- Failed upgrade.
- Workstation failure.
- Ransomware or local tampering.
- Accidental batch misconfiguration.

Recovery objectives must be configured by institution. V1 target: full system restore under 15 minutes for typical deployments subject to storage size.

## 7. Migration Process

Migration process:

1. Read current schema version.
2. Run pre-migration diagnostics.
3. Create migration backup.
4. Verify migration backup.
5. Apply migrations sequentially.
6. Rebuild derived indexes/reports if required.
7. Run post-migration diagnostics.
8. Record migration audit event.

## 8. Recovery Testing

Required tests:

- Restore quick backup to test location.
- Restore full backup to test location.
- Verify template and credential artifact integrity after restore.
- Verify audit log continuity.
- Verify application startup after restore.
- Verify sample credential search and print preview after restore.

## 9. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Backup appears successful but is unusable | Mandatory verification and periodic restore drills. |
| Backups stored on same failing disk | Administrator guidance and configurable external/local removable backup location. |
| Restore overwrites good data | Staging restore, current emergency backup, explicit confirmation. |
| Large asset store slows backup | Incremental strategy planned, progress UI, scheduled backup windows. |
| Migration failure | Verified migration backup and restore-only rollback. |
