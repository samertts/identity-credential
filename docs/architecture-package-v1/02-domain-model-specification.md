# Document 2 — Domain Model Specification

## 1. Purpose

This document defines the core domain language, entities, aggregates, relationships, lifecycles, versioning strategy, and historical data strategy for UICMP.

## 2. Domain Principles

- The system manages universal identities, not only employees.
- The model must support persons, organizations, departments, memberships, and dynamic attributes.
- Credential and template versions are immutable once certified or used.
- No record is physically deleted through application behavior.
- Status transitions are explicit and audited.

## 3. Entities

| Entity | Purpose | Key Attributes |
|---|---|---|
| Entity | Universal identity subject; can be person, organization, or department | `entity_id`, `entity_type`, `display_name`, `status`, `created_at`, `updated_at`, `archived_at` |
| Person Profile | Person-specific details attached to Entity | names, DOB if configured, phone, email, identifiers, custom fields |
| Organization | Organization identity and hierarchy root | name, code, registration fields, status |
| Department | Department or sub-unit | organization, parent department, name, code |
| Membership | Historical relationship between person and organization/department | person, org, dept, title, start/end, status |
| Credential Type | Configurable class of credential | name, validity policy, required fields, approval policy |
| Credential | Issuable credential aggregate | entity, type, lifecycle state, current version, expiry |
| Credential Version | Immutable generated/printed credential revision | card number, template version, generated assets, issue/expiry dates |
| Template | Logical template family | name, category, orientation, dimensions, status |
| Template Version | Immutable template design revision | layout, fields, assets, certification status/hash |
| Policy | Configurable rule bundle | name, version, conditions, actions, effective dates |
| Photo | Original and processed photo metadata | subject, hashes, quality score, versions |
| Asset | Logo, watermark, font, background, icon | type, storage path, fingerprint, license/owner |
| Audit Log | Append-only accountability record | actor, action, target, before/after hash, timestamp |
| User | Local application user | username, status, password hash or local auth reference |
| Role | RBAC role | operator, reviewer, approver, printer, administrator |
| Permission | Atomic privilege | module/action/resource |
| Event | Durable local domain/application event | event type, payload, status, retries |
| Backup | Backup metadata | type, path, hash, status, verification result |
| Report | Saved report definition/output metadata | report type, parameters, generated file |

## 4. Aggregates

### 4.1 Identity Aggregate

Root: `Entity`

Children:

- Person profile
- Dynamic attributes
- Membership references
- Photo references

Invariant: an entity cannot be archived while active credentials exist unless the archive workflow first expires, revokes, or archives credentials according to policy.

### 4.2 Membership Aggregate

Root: `Membership`

Invariant: membership dates must not produce impossible history. Overlaps are allowed only when policy permits multiple concurrent roles.

### 4.3 Credential Aggregate

Root: `Credential`

Children:

- Credential versions
- Approval records
- Print history
- QR payload records

Invariant: credential generation requires an approved credential and a certified template version.

### 4.4 Template Aggregate

Root: `Template`

Children:

- Template versions
- Template components
- Certification records
- Packaging records

Invariant: a published template version is immutable.

### 4.5 Photo Aggregate

Root: `Photo`

Children:

- Original file record
- Processed file versions
- Quality analysis records

Invariant: original photo is preserved even when processed versions change.

### 4.6 Security Aggregate

Root: `User`

Children:

- User roles
- Permission assignments
- Authentication events

Invariant: maker-checker duties require different users for creation/submission and approval where policy demands it.

## 5. Relationships

```text
Organization 1..n Department
Entity(Person) 1..n Membership
Membership n..1 Organization
Membership n..0 Department
Entity 1..n Credential
Credential 1..n CredentialVersion
CredentialVersion n..1 TemplateVersion
Template 1..n TemplateVersion
Entity 1..n Photo
Photo 1..n PhotoVersion
User n..m Role
Role n..m Permission
All auditable records 1..n AuditLog
```

## 6. Lifecycle Definitions

### 6.1 Credential Lifecycle

```text
Draft -> Review -> Approved -> Generated -> Printed -> Active -> Expired -> Archived
                         |             |           |        |
                         v             v           v        v
                      Revoked       Revoked     Revoked  Revoked
```

Rules:

- `Draft`: editable by authorized operators.
- `Review`: locked except reviewer comments and return-to-draft action.
- `Approved`: eligible for generation.
- `Generated`: PNG/PDF exists and is fingerprinted.
- `Printed`: print job completed and recorded.
- `Active`: credential is valid for use.
- `Expired`: validity date passed or expiry job applied.
- `Revoked`: invalidated before expiry.
- `Archived`: retained for history; not operationally active.

### 6.2 Template Lifecycle

```text
Draft -> Validated -> Certified -> Published -> Archived
       -> Rejected/Returned for edits
```

Rules:

- Draft template may change.
- Validated template passes structural validation.
- Certified template receives integrity hash and certifier record.
- Published template is selectable for credential generation.
- Archived template remains available for historical render verification.

### 6.3 Photo Lifecycle

```text
Imported/Captured -> Analyzed -> Processed -> Approved -> Superseded/Archived
```

Original photo preservation is mandatory.

## 7. Versioning Strategy

Versioned records contain:

- Stable logical ID.
- Version number.
- Effective dates where applicable.
- Created/updated metadata.
- Superseded reference.
- Integrity hash for sensitive records.

Version increments occur when a business-significant change affects issued credentials, templates, policies, photos, or configuration. Minor UI-only metadata does not create domain versions unless audit policy requires it.

## 8. Historical Data Strategy

- Use append-only history tables for sensitive aggregates.
- Retain generated credential artifacts by version.
- Retain original and processed photos.
- Retain template packages used for issued credentials.
- Retain all audit logs according to institutional retention policy.
- Archive rather than delete obsolete records.

## 9. Domain Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Employee-centric assumptions | Use universal Entity and Membership model with dynamic attributes. |
| Unbounded custom fields | Validate custom field definitions, data types, required flags, and search indexing policy. |
| Lifecycle ambiguity | Formal transition matrix and approval policy per credential type. |
| Historical reconstruction failure | Store version references on credential versions and generated artifacts. |
| Regulatory retention conflicts | Make retention policy configurable while preserving no-physical-delete default. |
