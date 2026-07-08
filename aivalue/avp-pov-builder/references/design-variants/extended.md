# Design Variant — Extended

A named design override for the Extended styling lineage (v3 most recent at 2026-05-25). **Do not apply to other engagements** unless the user explicitly invokes this variant at intake.

---

## When to apply

User selects "Extended variant" at intake (per `intake-checklist.md` Q22 — Design variant). Apply only on explicit user request. This variant provides an extended palette with greens, custom dark navy, and includes Strategy and MonteCarlo tabs.

---

## What this variant overrides

The Extended variant is **a palette and structural extension**, not a full styling rewrite. It departs from canonical in three areas:

### 1. Extended palette

The Extended variant adds non-canonical accent colors to the standard Slalom palette:

| Extended color added | Hex | Role |
|---|---|---|
| Mid-green | `#5BA85B` | Positive accent / success-light |
| Dark green | `#1a6e2e` | Severity-low pill text, positive emphasis |
| Light pink | `#FF9FAB` | Tertiary coral accent |
| Dark coral | `#c0283a` | Severity-high pill text |
| Dark navy | `#1a1a2e` | Replaces `--dark-blue` in some hero contexts — softer than Slalom dark blue |

The standard canonical palette is retained — the Extended variant *adds* these accents rather than replacing the canonical set.

**Note:** the mid-green (`#5BA85B`) was originally added in v2.4 for the now-removed Risks tab severity-low pill; the Extended variant repurposes it as a broader positive accent.

### 2. Generic system font stack

The Extended variant uses a system font stack rather than a brand-specific lineage:

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

Trade-off: faster first paint, no external font dependency. The visual lineage is cleaner and less Slalom-brand-heavy.

### 3. Additional tabs — Strategy and Monte Carlo

The Extended variant includes two additional tabs beyond the canonical 7-tab default:

- **Strategy** (`tab-strategy`) — a dedicated strategy framing tab in front of AI Portfolio. Used when the audience requires more strategic context than the Why Now tab provides alone.
- **Monte Carlo** (`tab-montecarlo`) — a dedicated MC results tab in addition to (not replacing) the portfolio-confidence section on the Assumptions tab. Used when the audience wants probabilistic ranges as their own deep-dive surface.

Both tabs are **opt-in extensions** for Extended-variant builds; they do not appear in the canonical 7-tab default. When the Extended variant is active, the tab count expands to 9 (or 7 in the 5-tab variant equivalent).

---

## What canonical rules still apply

- The canonical 7 tabs are all present (Summary · Why Now · AI Portfolio · AVP Analysis · Roadmap · Assumptions · Sources) — Strategy and Monte Carlo are *additions*, not replacements
- Tab IDs are canonical for the standard 7 (`tab-summary`, `tab-whynow`, etc.); additional Extended variant tabs use `tab-strategy` and `tab-montecarlo`
- Content discipline from `editorial-rules.md` applies
- QA checklist (`qa-checklist.md`) applies — extend the panel-placement check to include `tab-strategy` and `tab-montecarlo`
- Accessibility (`design.md` — 27) applies

---

## Reference build

The reference build for this variant lives in the engagement project folder. Update this path when the reference build is refreshed.

---

## Anti-patterns

- Using the Extended variant dark navy (`#1a1a2e`) in place of `--dark-blue` (`#002FAF`) in canonical builds — they're not interchangeable, and the canonical hero gradient depends on `--dark-blue`
- Adding Strategy/Monte Carlo tabs to non-Extended builds without explicit user request
