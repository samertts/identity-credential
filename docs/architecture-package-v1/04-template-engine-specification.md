# Document 4 — Template Engine Specification

## 1. Purpose

The Template Engine is a universal credential layout system supporting front/back designs, text, images, QR, barcode, date fields, shapes, logos, watermarks, layers, grouping, locking, snapping, guides, preview, validation, packaging, certification, and versioning.

## 2. Template Model

Template attributes:

- Template ID
- Name and category
- Credential type compatibility
- Orientation: portrait or landscape
- Media type: PVC, A4, custom
- Side support: front, back, double-sided
- Dimensions and units
- Bleed, safe area, margins
- Version list
- Status
- Owner and certification metadata

Template version attributes:

- Version number
- Layout JSON
- Required data bindings
- Asset references and hashes
- Validation result
- Certification hash
- Certifier and certification timestamp
- Compatibility range

## 3. Element Types

- Text field
- Image field
- Photo field
- QR field
- Barcode field
- Date field
- Shape
- Line
- Logo
- Watermark
- Static image
- Conditional element
- Group/container

Common element properties:

- `element_id`
- `name`
- `type`
- `x`, `y`, `width`, `height`
- `rotation`
- `z_index`
- `opacity`
- `locked`
- `visible`
- `binding`
- `style`
- `validation_rules`

## 4. Layer System

Layer features:

- Ordered z-index layers.
- Lock/unlock layer.
- Hide/show layer.
- Group and ungroup elements.
- Alignment and distribution commands.
- Snap to grid and guides.
- Background and watermark layers protected from accidental editing.

Layer constraints:

- QR layer must remain printable and scannable.
- Required photo fields cannot be hidden in certified templates.
- Locked certified templates cannot be edited; edits create a new draft version.

## 5. Rendering System

Rendering pipeline:

```text
Load TemplateVersion
 -> Verify certification if production render
 -> Resolve data bindings
 -> Validate required fields
 -> Render front side canvas
 -> Render back side canvas if configured
 -> Generate QR/barcode locally
 -> Compose assets with fingerprints
 -> Output PNG and/or PDF
 -> Fingerprint output artifacts
```

Rendering outputs:

- PNG front
- PNG back
- PDF credential file
- A4 layout PDF
- Preview image

Rendering rules:

- Preview may use draft templates but must show watermark when uncertified.
- Production credential generation requires a certified template version.
- Rendering must be deterministic for the same template version and data snapshot.

## 6. Validation System

Validation categories:

- Structural: dimensions, sides, required layers, safe areas.
- Binding: all required fields resolve to allowed data sources.
- Asset: referenced assets exist and hashes match.
- QR: mandatory QR exists and meets size/error correction policy.
- Print: safe area, bleed, DPI, color settings.
- Security: no forbidden script/network references.
- Accessibility/usability: text contrast, minimum font sizes where policy requires.

Validation result states:

- Passed
- Warning
- Failed

Warnings do not block draft preview but may block certification depending on policy.

## 7. Certification Workflow

```text
Designer creates draft
 -> Validate template
 -> Reviewer inspects preview and validation report
 -> Certifier certifies version
 -> System computes certification hash
 -> Template version becomes immutable
 -> Administrator publishes version
```

Certification record includes:

- Template version ID
- Validation report hash
- Asset hash bundle
- Certifier user ID
- Certification timestamp
- Certification decision
- Comments

## 8. Versioning Workflow

- Editing a certified or published version creates a new draft version.
- New versions copy layout and asset references from parent.
- Old versions remain available for historical credential reconstruction.
- Credential versions reference the exact template version used.

## 9. Packaging Format

Template package archive:

```text
template-package.uicmp-template
├── manifest.json
├── template.json
├── assets/
├── validation-report.json
├── certification.json
└── hashes.json
```

Package manifest fields:

- `package_version`
- `template_id`
- `template_version`
- `category`
- `dimensions`
- `required_bindings`
- `asset_hashes`
- `certification_hash`
- `exported_at`
- `exported_by`

## 10. Initial Template Library Requirement

V1 must ship with at least 25 templates across Employee, Visitor, Contractor, Trainee, Conference, VIP, Temporary, Committee, Official, and Generic categories. The library must include portrait, landscape, single-side, double-side, A4, and PVC layouts.

## 11. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Unscannable QR due to design choices | Mandatory QR validation, minimum size, contrast checks, print test certification. |
| Asset tampering after certification | Asset fingerprints included in certification hash. |
| Template sprawl | Category governance, archive workflow, search metadata, published-version controls. |
| Designer complexity | Quick templates, component library, validation guidance, undo/redo. |
| Historical render mismatch | Credential versions pin template version, data snapshot, asset hashes, and output hashes. |
