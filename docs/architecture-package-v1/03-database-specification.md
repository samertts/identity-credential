# Document 3 — Database Specification

## 1. Purpose

UICMP V1 stores operational data in SQLite. The schema must remain compatible with future migration to PostgreSQL or SQL Server by avoiding SQLite-only business assumptions in application logic.

## 2. Database Principles

- SQLAlchemy owns mappings and migrations.
- UI never accesses database sessions.
- All tables include logical archive/status fields where applicable.
- Sensitive tables include integrity hashes.
- Audit logs are append-only.
- Foreign keys are enabled in SQLite.
- Application behavior never physically deletes business records.

## 3. Common Columns

Most business tables include:

| Column | Type | Notes |
|---|---|---|
| `id` | UUID text | Primary key |
| `version` | integer | Starts at 1 |
| `status` | text | Active, archived, draft, etc. |
| `created_at` | datetime | UTC |
| `created_by` | UUID text | Nullable for system seed data |
| `updated_at` | datetime | UTC |
| `updated_by` | UUID text | Nullable for system automation |
| `archived_at` | datetime | Null unless archived |
| `archived_by` | UUID text | Null unless archived |
| `integrity_hash` | text | Required for sensitive/versioned records |

## 4. Core Tables

### 4.1 Identity Tables

#### `entities`

- `id` PK
- `entity_type` check: person, organization, department, external_party
- `display_name`
- `status`
- common columns

Indexes:

- `idx_entities_type_status`
- `idx_entities_display_name`

#### `person_profiles`

- `id` PK
- `entity_id` FK `entities.id`, unique
- `given_name`
- `middle_name`
- `family_name`
- `preferred_name`
- `date_of_birth` nullable and policy-controlled
- `phone`
- `email`
- common columns

#### `organizations`

- `id` PK
- `entity_id` FK `entities.id`, unique
- `code` unique
- `name`
- `legal_name`
- common columns

#### `departments`

- `id` PK
- `entity_id` FK `entities.id`, unique
- `organization_id` FK `organizations.id`
- `parent_department_id` FK `departments.id` nullable
- `code`
- `name`
- common columns

Unique constraint: `(organization_id, code)`.

#### `memberships`

- `id` PK
- `person_entity_id` FK `entities.id`
- `organization_id` FK
- `department_id` FK nullable
- `job_title`
- `membership_type`
- `start_date`
- `end_date`
- `status`
- common columns

Indexes:

- `idx_memberships_person_status`
- `idx_memberships_org_dept`
- `idx_memberships_dates`

#### `custom_field_definitions`

- `id` PK
- `scope` text
- `field_key` text
- `label`
- `data_type`
- `required` boolean
- `searchable` boolean
- `validation_rules_json`
- common columns

Unique constraint: `(scope, field_key, version)`.

#### `custom_field_values`

- `id` PK
- `definition_id` FK
- `target_type`
- `target_id`
- `value_text`
- `value_number`
- `value_date`
- `value_json`
- common columns

Index: `(target_type, target_id)`.

### 4.2 Credential Tables

#### `credential_types`

- `id` PK
- `code` unique
- `name`
- `description`
- `validity_policy_json`
- `approval_policy_json`
- `template_selection_policy_json`
- common columns

#### `credentials`

- `id` PK
- `entity_id` FK
- `credential_type_id` FK
- `state`
- `current_version_id` FK nullable
- `card_number` unique nullable until generated
- `issue_date`
- `expiry_date`
- common columns

Indexes:

- `idx_credentials_entity_state`
- `idx_credentials_card_number`
- `idx_credentials_expiry_state`

#### `credential_versions`

- `id` PK
- `credential_id` FK
- `version_number`
- `template_version_id` FK
- `qr_payload_hash`
- `png_asset_id` FK nullable
- `pdf_asset_id` FK nullable
- `generated_at`
- `generated_by`
- `certification_status`
- common columns

Unique constraint: `(credential_id, version_number)`.

#### `credential_approvals`

- `id` PK
- `credential_id` FK
- `requested_by` FK users
- `reviewed_by` FK users nullable
- `approved_by` FK users nullable
- `decision`
- `comments`
- `decided_at`
- common columns

#### `print_jobs`

- `id` PK
- `credential_version_id` FK nullable for batch container jobs
- `printer_profile_id` FK
- `job_type`
- `status`
- `requested_by`
- `started_at`
- `completed_at`
- `failure_reason`
- common columns

#### `print_job_items`

- `id` PK
- `print_job_id` FK
- `credential_version_id` FK
- `sequence_number`
- `status`
- `reprint_reason` nullable
- common columns

### 4.3 Template Tables

- `templates`
- `template_versions`
- `template_components`
- `template_assets`
- `template_certifications`
- `template_packages`

Key indexes:

- `idx_templates_category_status`
- `idx_template_versions_template_status`
- `idx_template_versions_hash`

### 4.4 Photo and Asset Tables

- `photos`
- `photo_versions`
- `photo_quality_results`
- `assets`
- `asset_fingerprints`

Asset uniqueness: `(fingerprint_hash, asset_type)`.

### 4.5 Security Tables

- `users`
- `roles`
- `permissions`
- `user_roles`
- `role_permissions`
- `sessions`
- `security_events`

Unique constraints:

- `users.username`
- `roles.code`
- `permissions.code`

### 4.6 Audit and Event Tables

#### `audit_logs`

- `id` PK
- `timestamp`
- `actor_user_id`
- `actor_role_snapshot_json`
- `action`
- `target_type`
- `target_id`
- `before_hash`
- `after_hash`
- `reason`
- `workstation_id`
- `correlation_id`
- `integrity_hash`

Indexes:

- `idx_audit_timestamp`
- `idx_audit_actor`
- `idx_audit_target`
- `idx_audit_action`

#### `event_log`

- `id` PK
- `event_type`
- `payload_json`
- `status`
- `retry_count`
- `created_at`
- `processed_at`
- `last_error`

### 4.7 Backup, Import, Export, Report, Diagnostic Tables

- `backup_records`
- `restore_records`
- `import_batches`
- `import_batch_items`
- `export_batches`
- `reports`
- `diagnostic_runs`
- `diagnostic_findings`

## 5. History Tables

History tables mirror high-risk business tables and append snapshots on change:

- `entity_history`
- `membership_history`
- `credential_history`
- `credential_version_history`
- `template_version_history`
- `photo_history`
- `policy_history`
- `configuration_history`

History records contain `history_id`, `source_id`, `source_version`, `change_type`, `snapshot_json`, `changed_at`, `changed_by`, and `integrity_hash`.

## 6. Backup Strategy at Database Level

- Use SQLite online backup API for quick backups.
- Full backups include database, assets, templates, generated files, logs, and manifest.
- Backup manifest stores file hashes, schema version, application version, and backup type.
- Backups are verified immediately after creation.

## 7. Constraints and Migration Concerns

- Use application-generated UUIDs to ease migration.
- Avoid relying on SQLite rowid semantics.
- Store timestamps in UTC.
- Use JSON text for flexible policies but validate through application schemas.
- Maintain explicit indexes for search and reports.

## 8. Database Risks and Mitigations

| Risk | Mitigation |
|---|---|
| SQLite file corruption | Regular verified backups, integrity checks, WAL, safe shutdown handling. |
| Large audit tables slowing reports | Indexed columns, report snapshots, archive partitions in future DB migration. |
| Dynamic fields becoming unqueryable | Searchable flag, typed value columns, controlled indexing. |
| Schema drift across plugins | Plugin migrations reviewed and namespaced; no plugin direct schema mutation without manifest approval. |
| Accidental physical deletes | Repository policy, restricted DB access, test coverage, triggers considered for critical tables. |
