# Document 6 — Photo Intelligence Specification

## 1. Purpose

The Photo Intelligence Engine captures, imports, analyzes, processes, versions, and preserves identity photos while retaining originals and providing quality scoring for credential readiness.

## 2. Capture

Supported capture sources:

- Local camera device.
- Local image file upload.
- Folder-based import.

Camera capture requirements:

- Device selection.
- Preview.
- Capture confirmation.
- Retake support.
- No cloud camera services.

## 3. Import

Import modes:

- Single file import.
- Batch folder import.
- Import wizard with matching rules.

Photo matching options:

- Filename to entity code.
- Filename to card number/import identifier.
- CSV/Excel mapping reference.
- Manual unresolved queue.

## 4. Face Detection

Face detection requirements:

- Local OpenCV-based processing.
- Detect zero, one, or multiple faces.
- Flag multiple faces as review required.
- Store detection metadata and confidence.

## 5. Auto Crop

Auto crop requirements:

- Center face according to credential photo policy.
- Maintain required aspect ratio.
- Preserve original image.
- Store crop parameters as version metadata.
- Allow manual override by authorized users.

## 6. Background Removal

V1 supports background removal as a configurable local processing capability. If quality is insufficient, the system must allow manual acceptance/rejection and retain both original and processed versions.

## 7. Quality Analysis

Quality metrics:

- Face detected.
- Face centered.
- Resolution sufficient.
- Brightness acceptable.
- Blur score acceptable.
- Contrast acceptable.
- Background acceptable where policy applies.
- File integrity hash valid.

Quality result:

- Score 0–100.
- Pass/warn/fail status.
- Metric-level findings.
- Recommendation text.

## 8. Storage Strategy

Storage layout:

```text
storage/photos/
├── originals/{entity_id}/{photo_id}/original.ext
├── processed/{entity_id}/{photo_id}/{version}.png
└── thumbnails/{entity_id}/{photo_id}/{version}.jpg
```

Database records store paths, hashes, dimensions, MIME type, source, and processing metadata.

## 9. Versioning

- Original photo is immutable.
- Each processed output is a new photo version.
- Credential versions reference the processed photo version used.
- Superseded photos remain available for historical credential reconstruction.

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| False face detection | Manual review queue and override with audit. |
| Poor photo quality reaching production | Credential validation checks approved photo version and minimum quality score. |
| Large photo storage growth | Thumbnail generation, storage diagnostics, backup rotation planning; no destructive deletion by default. |
| Privacy exposure | RBAC, local storage only, audit access, encrypted backup option. |
| Original loss | Immutable original preservation and hash verification. |
