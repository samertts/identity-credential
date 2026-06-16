# Document 5 — Printing Engine Specification

## 1. Purpose

The Printing Engine is separate from the Generation Engine. Generation creates fingerprinted PNG/PDF artifacts. Printing manages printer profiles, preview, queueing, print history, reprint controls, A4 layout, and batch printing.

## 2. Generation Outputs

Supported generation outputs:

- PNG front side
- PNG back side
- Combined PDF
- A4 layout PDF
- Preview thumbnails

Each artifact stores:

- File path
- File type
- Credential version
- Hash
- Generated timestamp
- Generator version

## 3. PDF Generation

PDF generation uses local rendering libraries and must support:

- PVC card dimensions.
- A4 layouts with multiple cards per sheet.
- Front/back layout for duplex or manual flip workflows.
- Metadata describing credential version and template version.
- Embedded images only from local approved assets.

## 4. PNG Generation

PNG generation must support:

- Configurable DPI.
- Transparent or solid backgrounds as template requires.
- Front/back separate files.
- Fingerprinting after write.
- Preview and production quality modes.

## 5. A4 Layout Engine

A4 layout responsibilities:

- Arrange multiple credentials per page.
- Support crop marks, spacing, margins, and labels.
- Support single-side and front/back manual workflows.
- Validate that page layout fits selected media.
- Store layout profile version with the print job.

## 6. Batch Printing

Batch workflow:

```text
User selects batch criteria
 -> System validates selected credentials
 -> Optional backup prompt
 -> Generate missing artifacts
 -> Create print job and items
 -> Preview summary
 -> Send to printer or export print PDF
 -> Track item-level status
 -> Produce batch report
```

Batch controls:

- Maximum batch size policy.
- Pause/resume/cancel where safe.
- Item-level retry.
- Failure isolation.
- Progress and audit events.

## 7. Printer Profiles

Printer profile fields:

- Profile ID
- Name
- Printer name
- Media type
- DPI
- Orientation
- Duplex setting
- Color mode
- Margins/calibration offsets
- A4 layout profile
- Default for credential types
- Status and version

Printer profiles are versioned because historical print reconstruction must know the profile used.

## 8. Print Queue

Print queue states:

- Pending
- Preparing
- Ready
- Printing
- Completed
- Failed
- Canceled
- Held

Queue rules:

- Only users with Printer or Administrator role can release print jobs.
- Print jobs record operator, workstation, printer profile, and artifact hashes.
- Failed jobs retain failure reason and diagnostics.

## 9. Reprint Strategy

Reprint requires:

- Permission.
- Reason code.
- Link to original credential version.
- Optional approval depending on policy.
- Audit record.
- Reprint count and print history entry.

Reprint never mutates the original print record.

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Printer driver inconsistency | Profile calibration, preview, test print, administrator-managed profiles. |
| Unauthorized reprints | RBAC, reason codes, approval policy, audit reports. |
| Batch failure halfway | Item-level statuses, retry, generated artifact retention, batch reports. |
| Generation/printing confusion | Strict service separation and artifact fingerprinting. |
| Poor A4 alignment | Calibration offsets and printable area validation. |
