# Portfolio View Toggle — Prioritized ↔ All Evaluated

A first-class view toggle on the AI Portfolio tab that lets the user (and viewer) swap between two pools: the **final portfolio** (8–25 UCs recommended) and **all evaluated candidates** (the full broad pool including 25–30 deprioritized).

## Why this exists

The skill's standard downselect produces a final portfolio of 8–25 from a broad pool of ~50. The deprioritized 25–30 normally live in a small "evaluated but deprioritized" panel beneath the matrix. That hides the rigor — clients see the final number and assume Slalom only sized that subset.

The toggle exposes the full broad-pool analysis as a first-class view so the dashboard can show both *"here's our recommendation"* and *"here's the complete evaluation set we ran."* For the Slalom PoV positioning, *"here's what we recommend — and here's everything we considered"* is more defensible than a final-number-only view. Procurement teams with experienced reviewers will ask why specific things aren't in the portfolio; the toggle answers that question before it's asked.

---

## UX

Two stacked buttons at the top of the function-filter sidebar, above the existing "Filter by function" controls:

- **Prioritized use cases** — *{N} from broad pool* (default, active on load)
- **All evaluated use cases** — *{N+M} broad-pool candidates (incl. {M} deprioritized)*

The view toggle and the function filter are both **sticky/persistent across tabs** and **compose**: view determines the pool; function filter is applied on top.

---

## Behavior across the dashboard when toggled

1. **Hero KPIs swap to per-view × per-function totals** — annual value, P50 NPV, count, implementation. Bridge sentence "X use cases" recalculates.
2. **AI Portfolio matrix bubbles**:
   - Prioritized bubbles render in function colors with solid borders.
   - Deprioritized bubbles render grey, dashed, smaller.
   - In **Prioritized** view, deprioritized bubbles are hidden (`display:none`).
   - In **All Evaluated** view, deprioritized bubbles appear.
   - Matrix axes (X = relative LOE percentile, Y = annual value) are computed **across both pools** so the axis range doesn't shift between views.
3. **Sidebar function buttons** — count and `$X M/yr*` value labels rewrite to match the current view's pool totals.
4. **Deprioritized panel styling promotes** from muted (Prioritized view: `opacity: 0.85`) to emphasized (All Evaluated view: `2px solid var(--slalom-blue)` + tinted header).
5. **Optional `.if-view-prio` / `.if-view-all` utility classes** let any block of copy be view-specific — e.g., a methodology paragraph that reads differently when "All Evaluated" is selected.

---

## Implementation pattern

### Data

Build a single `FN_DATA` JSON dict keyed `{view: {fn: {ab, npv, count, impl, label}}}` where `view ∈ {"prio","all"}` and `fn ∈ {"ALL","F1","F2","F3","F4"}`. Emit it inline as a JS `const` so toggle/filter can read totals without re-fetching.

### CSS state

Two body-level classes (`body.view-prio` and `body.view-all`) drive everything via CSS. **Never inline styles for visibility.** Rules:

```css
body.view-prio .deprio-bubble { display: none }
body.view-prio .if-view-all   { display: none }
body.view-prio .deprio-panel  { opacity: 0.85 }

body.view-all .deprio-bubble  { display: initial }
body.view-all .if-view-prio   { display: none }
body.view-all .deprio-panel   { border: 2px solid var(--slalom-blue); opacity: 1 }
```

### JS

Single `setView(view)` function:

1. Toggle body class (`view-prio` ↔ `view-all`).
2. Toggle button active state.
3. Rewrite sidebar count/value labels from `FN_DATA[view]`.
4. Call `filterFn(CURRENT_FN)` so the function filter re-applies cleanly against the new pool.

`filterFn` reads `CURRENT_VIEW` when computing hero swaps so the two states **compose**.

### Matrix SVG

Both pools are passed into the SVG builder. Y-max and X-range are computed from the **union** so bubbles don't reflow when the view changes. Deprioritized bubbles are emitted with class `uc-bubble deprio-bubble` and **never get an onclick handler** — they're informational, not modal-bound.

---

## Defaults & guardrails

- Default view is `prio` on page load: `<body class="view-prio filter-ALL">`.
- **If the broad pool equals the final portfolio (downselect ratio = 1.0), suppress the toggle entirely.** A single-state toggle is noise — render the standard sidebar without it.
- The "All Evaluated" view must **never claim the dashboard recommends the deprioritized items.** Copy in the deprioritized panel keeps the *"evaluated and deprioritized — not ignored"* framing with reactivation triggers per UC. See `structural-rules.md` — Evaluated but deprioritized panel.
- The **Sources tab Monte Carlo paragraph** must say *"10,000 trials on all {broad-pool} candidates,"* not *"on the {final} portfolio"* — the toggle exists precisely because the rigor extends to the full pool.

---

## Where in the skill

Phase 7 → Phase 9 handoff:

- **Phase 7 (downselect)** must persist **both** `final_list` and `deprio` to `mc_results.json`, not just the final. Without the deprio list, the toggle has nothing to show in the "All Evaluated" state.
- **Phase 9 (HTML render)** wires:
  - The toggle component into the function-filter sidebar.
  - `FN_DATA` emission as inline JS const.
  - Dual-pool matrix SVG draw with union-computed axes.
  - The `body.view-prio` / `body.view-all` CSS rules.
  - The "All Evaluated"-specific copy via `.if-view-all` blocks where the methodology framing should shift.
- **Decisions log** (`decisions-{client}.md`) carries a parking-lot prompt for the explicit suppression decision when downselect ratio = 1.0 — see `decisions-log.md` — 3a — Portfolio view toggle.
