# Design Variant — Multifile

A named design override for the Multifile styling lineage. **Do not apply to other engagements** unless the user explicitly invokes this variant at intake.

---

## When to apply

User selects "Multifile variant" at intake (per `intake-checklist.md` Q22 — Design variant). Apply only on explicit user request.

---

## What this variant overrides

The Multifile variant is a **fully custom styling lineage**, not a palette tweak. It departs from canonical in three substantial ways:

### 1. Multi-file format

Canonical builds ship as a single self-contained HTML file with inline CSS and JS. The Multifile variant uses external stylesheets:

```html
<link rel="stylesheet" href="styles.css" />
<link rel="stylesheet" href="loop.css" />
<link rel="stylesheet" href="pages.css" />
```

Trade-off: portability lost (the dashboard is no longer a single file). Reason: the Multifile design lineage was built as a multi-asset page system, and forcing it into a single file would break its visual integrity.

### 2. Typography — DM Sans / DM Mono

Canonical uses system font stacks. The Multifile variant uses Google Fonts:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400;1,9..40,500&family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet" />
```

DM Sans for body and headings; DM Mono for numeric callouts and code-style accents.

### 3. Theme system — `data-theme` + `data-density`

The Multifile variant uses HTML data attributes to drive theme behavior:

```html
<html lang="en" data-theme="multifile" data-density="regular">
```

The `data-theme="multifile"` attribute scopes the entire styling tree. Removing it falls back to a different theme. The `data-density` attribute toggles compact / regular / loose spacing.

---

## What canonical rules still apply

- The 7-tab default structure is unchanged (Summary · Why Now · AI Portfolio · AVP Analysis · Roadmap · Assumptions · Sources)
- Tab IDs are canonical (`tab-summary`, `tab-whynow`, etc.)
- Content discipline from `editorial-rules.md` (sentence case, banned vocabulary, narrative cohesion) applies
- QA checklist (`qa-checklist.md`) applies — adapt the CSS-specific checks to the external stylesheet locations
- Accessibility (`design.md` — 27) applies — WCAG 2.1 AA is the floor regardless of variant

---

## Reference build

The reference build for this variant lives in the engagement project folder alongside its external CSS files (`styles.css`, `loop.css`, `pages.css`). Update this path when the reference build is refreshed.

---

## Anti-patterns

- Mixing canonical Slalom Blue (#0C62FB) with the DM Sans/DM Mono palette — the visual lineages don't blend cleanly
- Loading DM Sans/DM Mono externally without the `preconnect` hints (degrades first-render perceptibly)
- Inlining the Multifile variant CSS into the HTML (defeats the multi-file design)
- Applying this variant without explicit user request at intake
