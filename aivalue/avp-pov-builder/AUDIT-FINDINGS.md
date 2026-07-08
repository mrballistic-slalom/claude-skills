# Skill Audit — Redundancies & Conflicts Found

Findings from the full read-through of all 15 reference files + SKILL.md during the `design.md` extraction (May 2026).

---

## Redundancies resolved by the design.md extraction

These items appeared in multiple files and are now consolidated in `design.md` as the single source of truth:

1. **Nav bar CSS** — was in `structural-rules.md` AND `qa-checklist.md`. Now in `design.md` — 6 only; structural-rules cross-refs it; qa-checklist should cross-ref it (not updated in this pass).

2. **Hero visual spec** (gradient, font sizes, big-one sizing) — was in `structural-rules.md` — The Hero pattern, `financial-model.md` — Visual treatment, AND implicitly in `qa-checklist.md` — 6. Now in `design.md` — 8.

3. **Bubble chart interaction JS** — was in `structural-rules.md` — Bubble chart click-to-filter AND `portfolio-matrices.md` — Matrix interactivity — click-to-filter. Nearly identical code blocks. Now in `design.md` — 18 only. The `portfolio-matrices.md` copy should be trimmed to a cross-reference in a future pass.

4. **Disclaimer band visual spec** (amber colors) — was in `structural-rules.md` — The Disclaimer band AND `qa-checklist.md` — 5. Now in `design.md` — 7.

5. **Chart container heights** — was in `structural-rules.md` — HTML rendering requirements AND `portfolio-matrices.md` — Rendering rules. Now in `design.md` — 10.

6. **Classification overlay spec** — was in `structural-rules.md` — AI Portfolio tab AND `portfolio-matrices.md` — Classification overlay. Now in `design.md` — 10; both source files cross-ref it.

7. **Deprioritized candidate treatment** — was in `structural-rules.md` — AI Portfolio tab AND `portfolio-matrices.md` — Deprioritized candidates. Now in `design.md` — 10 and — 22.

8. **Editorial discipline summary at bottom of structural-rules.md** — was a verbatim copy of the editorial-rules.md quick cheat sheet. Removed from structural-rules.md entirely.

---

## Issues found and fixed

### 1. Modal section numbering mismatch (BUG — FIXED)

The tech-pill HTML template heading said `8. Technology stack` but the per-UC modal 10-section spec lists it as Section 9 ("Strategic anchors + technology & data"). Traced to the 16→10 section trim.

**Fix:** Updated heading in `design.md` — 13 to `9. Strategic anchors + technology & data`.

### 2. Phase 3 purple hex never stated explicitly (FIXED)

`portfolio-matrices.md` — Color encoding said "Phase 3 purple" without a hex value. The color is `#7B61FF` per the CSS variable `--purple` / `--foundational` in the design system.

**Fix:** Added `#7B61FF` explicitly in `portfolio-matrices.md`: "Phase 1 blue #0C62FB, Phase 2 teal #1BE1F2, Phase 3 purple #7B61FF".

### 3. Unmerged v2.1 addenda (FIXED)

Three files carried addenda appended at the bottom with "Append to the end of..." / "Insert after..." language rather than being integrated into the main body:

- **`intake-checklist.md`** — Q[N+1] through Q[N+4] renumbered as Q18–Q21 and merged into the main question sequence.
- **`classification-rules.md`** — "INFERRED derivation chains" section merged after the data model format section. "How we sized this" section trimmed to a cross-reference to `design.md` — 24 (was duplicated with `structural-rules.md`).
- **`benefit-classification.md`** — "Per-engagement class name overrides" section merged after the multi-industry examples. The two additional anti-patterns merged into the existing anti-patterns section. Cheat sheet updated with step 8.

All three files now read as continuous documents with no "append to..." instructions.

### 4. "How we sized this" cross-file duplication (FIXED)

The section was specified in both `structural-rules.md` and `classification-rules.md`. The structural-rules version (content requirement) is preserved with a cross-ref to `design.md` — 24 for the visual template. The classification-rules version is trimmed to a cross-ref to `design.md` — 24, keeping only the content requirement ("A UC without this section cannot ship").

---

## New addition: Accessibility (see 27 in design.md)

Added a comprehensive WCAG 2.1 AA accessibility section covering:
- Colour contrast audit of the full palette with known risks and remediations
- Semantic HTML requirements
- Keyboard navigation patterns
- Focus management (modal focus trap, tab switch focus)
- ARIA attributes for tab bars, modals, charts, tooltips, status pills
- Chart accessibility (canvas `aria-label` + table equivalents)
- Image alt text requirements
- `prefers-reduced-motion` media query
- Print accessibility
- QA checklist additions (10 new checks)

---

## Remaining items for future passes

All documented issues have been resolved. No known redundancies or conflicts remain.

Three items that were deferred in the initial pass have been fixed:
- `portfolio-matrices.md` rendering rules trimmed to cross-ref `design.md` for visual specs; addendum merged; duplicate JS removed
- `financial-model.md` hero visual treatment replaced with cross-ref to `design.md` — 8; v2.1 addendum merged (non-standard structures, realization factor calibration)
- `qa-checklist.md` header note added pointing to `design.md` as source of truth; accessibility checks (see 39) added

Three additional v2.1 addenda discovered and merged:
- `engagement-config.md` — 13 (financial structure), 14 (benefit class overrides), 15 (non-financial value) integrated into template and body
- `monte-carlo.md` — 6-metric composite ranking model replaced the original 5-metric table; addendum removed
- `portfolio-matrices.md` — click-to-filter addendum merged into the rendering rules section

---

## Summary

| Category | Count | Status |
|---|---|---|
| Redundancies resolved by design.md extraction | 8 | ✅ Done |
| Bugs found and fixed | 1 | ✅ Fixed |
| Underspecifications found and fixed | 1 | ✅ Fixed |
| Unmerged addenda | 7 files | ✅ Merged (intake, classification, benefit, portfolio-matrices, engagement-config, financial-model, monte-carlo) |
| Cross-file duplication trimmed | 2 | ✅ Fixed (classification + portfolio-matrices) |
| Accessibility section added | 1 | ✅ New (design.md — 27 + qa-checklist — 39) |
| QA checklist source-of-truth note | 1 | ✅ Added |
| Financial-model.md visual spec trimmed | 1 | ✅ Cross-ref to design.md |
