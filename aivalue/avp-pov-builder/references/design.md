# Design System

Visual and structural design specifications for every PoV dashboard. This file is the single source of truth for **how things look and behave** — colors, type, spacing, components, layout, interaction, and print fidelity.

**Relationship to other references:**
- `editorial-rules.md` — **how content reads**: narrative cohesion, banned vocabulary, repetition limits, heading conventions, disclaimer content, asterisk system, spell-outs, forcing-card taglines, narrative uniqueness
- `structural-rules.md` — **what content goes where**: tab structure, section ordering, per-UC modal 10-section spec, citation routing, fixed vs. flexible structure, forbidden content, standardized vocabularies
- `design.md` (this file) — **how it looks**: every CSS variable, component spec, layout rule, interaction pattern, and visual anti-pattern

When building or reviewing, read all three. When debugging a visual issue, start here.

---

## 1. Brand palette — CSS variables only

Define once in `:root`; reference via `var()` everywhere. Inline hex codes outside the variable system are forbidden.

### Primary

| Variable | Hex | Role |
|---|---|---|
| `--slalom-blue` | #0C62FB | Primary accent — eyebrows, citations, links, h2 color when consistency calls for it |
| `--dark-blue` | #002FAF | Hero background gradient start |

### Accent

| Variable | Hex | Role |
|---|---|---|
| `--coral` | #FF4D5F | "Top priority" / coral accent / warning |
| `--teal` | #1BE1F2 | Phase 1 / "quick win" / success-emerging accent; hero second-line color |
| `--purple` / `--foundational` | #7B61FF | "Foundational" / Phase 2 accent |
| `--teal-deep` | #0e7a86 | Muted teal accent (e.g., "incremental revenue" pill) |
| `--pos` | #1f7a1f | Positive / probability green |

### Neutrals

| Variable | Hex | Role |
|---|---|---|
| `--ink` | #0e1422 | Primary type color |
| `--ink-2` | #3b4458 | Secondary type color |
| `--muted` | #6b7588 | Tertiary type / de-emphasis |
| `--bg` | #F6F8FB | Page background |
| `--line` | #E3E7EE | Borders, dividers |
| `--card` | #FFFFFF | Card/surface background |
| `--surface-2` / `--rule` | #f6f7f9 / #e3e6ec | Secondary surface (glossary panel, muted blocks) |

### Status

| Variable | Hex | Role |
|---|---|---|
| `--amber` | #F5A623 | Disclaimer accent border |
| `--amber-bg` | #FFF3CD | Disclaimer band background |

### Colour rules

- One accent color per single section unless colors communicate distinct categories (e.g., 5 phase colors in a chart legend, function colors in a bridge)
- Gradient backgrounds reserved for hero only — all other surfaces use solid fills or tints
- Function colors are per-engagement, defined in `engagement-config.md` — 8 and consumed as CSS variables

---

## 2. Type scale — ≤9 sizes total

| Size | Role | Example selectors |
|---|---|---|
| 10px | Micro labels, eyebrows, citation chips, watermark text | `.sec-eye`, `.cite`, axis labels |
| 11px | Small caps, footnotes, small pills, table headers | `.kpi-row-label`, `<th>` styling |
| 12px | Small body, table cells, secondary text | `.bt-uses`, plan-col body |
| 13px | Default body, lead paragraphs, modal body | `<p>` default |
| 14px | Lead body, anchor card subtitles, h4-equivalents | `.lead`, card titles |
| 18px | h3 sub-section titles | `<h3>` |
| 22px | Modal stats, mid-headings | `.modal-stat .val`, `<h4>` in modal |
| 28px | h2 section titles, KPI numbers | `.sec-title`, `.kpi .val` |
| 56–80px (display) | Hero typography only | `.hero-headline`, `.hero-savings-num` |

**Forbidden:** half-step values (9.5, 10.5, 11.5, 12.5, 13.5, 22, 30) outside hero. The cumulative inconsistency reads as AI-assembled even when individual deltas are imperceptible.

**Hero exception:** the hero may use up to 3 distinct display sizes (e.g., 56 / 64 / 80) when they serve genuinely different roles (logo / headline / display number).

---

## 3. Spacing scale — 4-base

Use `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 80` exclusively for margins, paddings, gaps.

**Forbidden:** off-scale values (5, 6, 10, 14, 18, 22, 30) in section spacing. Snap them.

**Per-element exception:** chart-container heights, modal max-widths, line-heights, and other tightly-tuned values may use any pixel value — but everything else snaps.

### Section rhythm

- `<section> { padding: 48px 0 }` — major sections breathe
- `.disclaimer + section { padding-top: 48px }` — first section after disclaimer matches
- Avoid alternating section backgrounds. Whitespace as separator > chrome as separator.

### Visual closure

Every section should have visual closure — avoid sections that end abruptly with body text and no visual break before the next section:

- Consistent `<section>` padding (48px) — vertical rhythm provides closure
- A trailing footnote or caption when one is needed
- A subtle divider only when the layout *requires* one (rare)

---

## 4. Card system — ≤2 base patterns

| Pattern | When | Spec |
|---|---|---|
| **Standard card** | Narrative content, function cards, anchor cards, phase cards, pattern cards | `border-radius: 8px`, `padding: 16px`, `border: 1px solid var(--line)`, optional 4px accent border (top OR left) |
| **Compact card** | Chip-style breakdowns, definitions, dense data | `border-radius: 8px`, `padding: 14px`, `border: 1px solid var(--line)`, optional 4px accent border |

### Accent border rules

- Position (top vs. left) communicates relationship — pick one per card type and stay consistent
- Thickness: always 4px, never mixed with 5px or 3px
- Colour: from CSS variables, never inline hex

### Forbidden

- More than two base patterns
- Multiple border-radius values across cards (6, 8, 10 used inconsistently)
- Padding values not on the 4-base spacing scale

---

## 5. Chrome — minimise

Things that read as "dashboard chrome" and signal AI-assembly when overused:

- Watermarks (diagonal "ILLUSTRATIVE" overlays) — defensible if requested for legal reasons; otherwise remove
- Coloured top-borders on every card — makes everything look like a status indicator
- Ribbons, banners, gradients, multi-shadow effects
- Pills + badges + chips combined in the same component

### Rules

- One accent treatment per card type, not multiple
- Solid fills > gradients (gradient backgrounds reserved for hero only)
- Box-shadow used sparingly — once per element class, not stacked
- Hover effects: scale-up or background-tint, not both

---

## 6. Nav bar

Matches AVP native UI.

```css
.nav { background: #0C62FB; }           /* Slalom Blue — NOT #002FAF */
.tab-btn { padding: 10px 18px; }        /* slim height */
.tab-btn.active { border-bottom-color: #fff; }   /* white underline */
.tab-btn { color: rgba(255,255,255,.7); }        /* inactive text */
.nav-brand { padding: 0 20px; }
```

### Logo

Embed the inline SVG from `assets/slalom-logo-white-RGB.svg` directly inside `<span class="slalom-logo">`. The skill ships the canonical Slalom logo (white-fill, viewBox `0 0 216 56.1`); paste its `<svg>` element verbatim into the nav.

- **No filter is needed** — the source is already white, designed for dark backgrounds
- **Do not** use base64 data URIs
- **Do not** load from external URLs (offline failure)
- **Do not** approximate with `<text>` (off-brand)

### Nav title

Dashboard title (e.g., "Slalom PoV — AI-enabled operations at [client]") as a text element between the logo and the tab buttons. White text, 13px, font-weight 500, opacity 0.85.

---

## 7. Disclaimer band

Appears at the top of **every tab panel**.

- Background: `var(--amber-bg)` (#FFF3CD)
- Accent border: `var(--amber)` (#F5A623)
- Language calibrated to classification mix (see `classification-rules.md`)
- Always includes: "illustrative analysis only", "do not represent actual cost commitments", "validation through discovery required"
- "Note on scope:" and "Currency note:" stay inline — no carriage return after the colon
- Full disclaimer: 3 paragraphs (illustrative basis, methodology transparency, validation requirement)

**No diagonal watermark** — the disclaimer band carries the illustrative status; the visual watermark adds noise without informational value.

---

## 8. Hero

The hero is the entire content of the Summary tab. See `structural-rules.md` for content spec (options-driven build, narrative triangle, grounding requirements); this section covers the visual implementation.

### Background

- Dark blue gradient: `#002FAF → #0a3a8a`

### Title

- 60–72px, font-weight 700
- If two-line title, second line in teal (`var(--teal)`, #1BE1F2)

### The big-one metric

- 88–100px, font-weight 700
- Visually dominant over the 2×3 KPI strip below

### KPI strip (the supporting six)

- 2 rows of 3, with visible row labels
- **Order:** "What it delivers" first (top row), "What it costs" second (bottom row) — value before cost
- Every monetary KPI includes explicit timing modifier in sub-text: **(one-time)** / **(recurring annual)** / **(cumulative, after-tax)** / **(months)**

### Phase strip

Below the KPI strip — slim Phase 0 / 1 / 2 / 3 progress strip showing four-phase plan with use case counts. At-a-glance phasing without full tab depth.

### Phase 0 caveat

Visible at the bottom of the hero section — a readable caveat inside the hero box (not a disclaimer footer).

---

## 9. Portfolio bridge visual

Two-layer visual on the Why Now tab between the hero reference and strategic alignment.

### Scope waterfall (horizontal chain, centred)

- Nodes: [N] Operations assessed → [N] Key activities mapped → [N] AI enhancements identified → [N] Prioritised use cases → [value metric]
- Node values: 32px font, bold
- Node labels: 12px uppercase
- Final node: dark-capped (dark background, teal/cyan number)
- Arrows between nodes: 24px
- **Centred horizontally** in the container

### Function cards

- Colour-coded top border (distinct color per function from `engagement-config.md` — 8)
- Content: function name, use case count, feature count, task count, NPV or primary value, value driver label

### Phase investment/value cards

- Phase 0 grey, Phase 1 blue, Phase 2 teal
- Each: investment, primary value metric, avg payback, constituent use case list

---

## 10. Chart containers

**Every canvas needs a parent div with an explicit pixel height** — hard Chart.js requirement.

```html
<div style="position:relative;width:100%;height:360px">
  <canvas id="someChart"></canvas>
</div>
```

### Height guidance

| Chart type | Height |
|---|---|
| Portfolio matrices (AI Portfolio tab; any axis pair from `portfolio-matrices.md`) | 480px each |
| Function-level bar chart (3–7 categories) | 360px |
| Annual cash flow stacked bar (6 year columns) | 360px |
| Cumulative line chart (6 points) | 360px |

### Matrix rendering

Each matrix renders in its own section (separate canvas, not stacked as small multiples) with:

- **Title** (sentence case, ≤8 words) — the storytelling claim
- **Subtitle** — 2–3 takeaways, ≤180 chars total
- **Chart** at 480px height
- **Read-out paragraph** (≤80 words) below the chart

### Classification overlay (mandatory on every matrix)

- Bundles with ≥1 INFERRED line: striped/dashed bubble border
- All-BENCHMARK/CLIENT_DATA: solid border
- Legend in chart footer

### Deprioritized candidates

- 50% opacity, neutral grey, dashed border
- Present on every matrix — audience sees the evaluation surface, not just survivors

### Filter controls

Single filter row controls all matrices on the tab simultaneously — three composable dropdowns:

1. Function (All + each function)
2. Strategic anchor (All + each anchor)
3. Phase (All + Phase 1 + Phase 2 + Phase 3)

---

## 11. CSS tooltip component

Replaces native `title` attributes (which have a ~1s hover delay). All hover tooltips in the dashboard use this pattern.

```css
.vtt { position: relative; cursor: help; border-bottom: 1px dotted #999; }
.vtt .vtt-text {
  visibility: hidden; opacity: 0;
  background: #333; color: #fff; font-size: 11px; line-height: 1.4;
  padding: 8px 12px; border-radius: 6px;
  position: absolute; z-index: 300;
  bottom: calc(100% + 8px); left: 0;
  min-width: 250px; max-width: 400px;
  box-shadow: 0 4px 12px rgba(0,0,0,.25);
  transition: opacity .15s;
}
.vtt .vtt-text::after {
  content: ''; position: absolute; top: 100%; left: 20px;
  border: 6px solid transparent; border-top-color: #333;
}
.vtt:hover .vtt-text { visibility: visible; opacity: 1; }
```

### Usage

```html
<span class="vtt">Hover target text
  <span class="vtt-text">Tooltip content — appears instantly on hover</span>
</span>
```

### Where to apply

- Per-UC modal: variable names in the "How we sized this" table
- Per-UC modal: source legend (S# / B# / I# definitions)
- Per-UC modal: `[formula]` link next to the modeled benefit metric
- Anywhere the dashboard references a term that benefits from inline explanation

**Never use native `title` attributes for interactive content.** Reserve `title` only for accessibility on icons and badges where screen readers need it.

---

## 12. Modal sizing

- Max-width: 1000px
- Max-height: 88vh
- Scrollable interior
- Depth is intentional — the executive scan happens on the tab; the analytical defence happens in the modal

**Modals are for Slalom-proposed (net-new) UCs only.** In-flight initiatives are acknowledged as cards on the Why Now tab — not modal-clickable.

---

## 13. Tech-pill treatment (UC modals)

In every per-UC modal Section 9 (Strategic anchors + technology & data), each `tech-pill` carries either a solid or dashed border based on the engagement's existing stack baseline (`engagement-config.md` — 3).

```html
<h4>9. Strategic anchors + technology & data
  <span class="tech-stack-legend">— solid = already in stack · dashed = net-new for this UC</span>
</h4>
<div class="tech-stack">
  <span class="tech-pill" title="Already in stack">Salesforce Einstein</span>
  <span class="tech-pill" title="Already in stack">Azure ML</span>
  <span class="tech-pill tech-pill-new" title="Net-new for this use case">Custom anomaly detection model</span>
</div>
```

```css
.tech-pill-new {
  border-style: dashed !important;
}
.tech-pill-new::before {
  content: "+ ";
  font-weight: 700;
  color: var(--slalom-blue, #0C62FB);
  margin-right: 2px;
}
```

Classification at render time: every `<span class="tech-pill">` text content is matched against the `existing_stack` keyword list from `engagement-config.md`. Match = solid; no match = dashed.

---

## 14. In-flight visual treatment

### Card treatment (Mode A — acknowledge only)

- Muted accent or neutral border — visually distinct from the proposal portfolio's UC cards on the AI Portfolio tab
- Cards are **NOT** clickable to modals — they're acknowledgments, not proposals
- Status pill on each card: *in production / in deployment / active collaboration / in build / announced for launch*

### Status legend

Rendered immediately under the in-flight section's lead paragraph:

```html
<div class="inflight-legend">
  <strong>Status legend:</strong>
  <span><strong>In production</strong> — live and benefiting users today</span>
  <span><strong>Rolling out</strong> — deployment in progress across the user base</span>
  <span><strong>Pilot</strong> — internal limited-scope live test</span>
  <span><strong>Vendor pilot</strong> — vendor-led trial against archetype data</span>
  <span><strong>Vendor evaluation</strong> — under technical / commercial assessment, not yet piloted</span>
</div>
```

Render only statuses that appear in the engagement's in-flight cards.

### Mode C — include in analysis (visual distinction)

| Element | Net-new | In-flight |
|---|---|---|
| Table row | Normal | "In flight" badge (green background) |
| Bubble chart | Solid fill | Dashed border + solid fill |
| Modal | Normal | "In flight" badge at top |
| KPI scope card | Count as net-new | Count separately: "N + M" |
| Phase strip | Included in phase counts | Included in phase counts |
| Roadmap chart | Included in cumulative lines | Included in cumulative lines |

### Optional in-flight strip (AI Portfolio tab, above the first matrix)

Non-clickable horizontal strip listing in-flight initiatives by name + status pill. Muted styling (smaller type, subtle background) — visual reminder without competing with chart content.

---

## 15. Anchor tooltips

Every body reference to an anchor code (`Anchor: A1`, `Anchor: A2, A3`, `[A4]`, etc.) carries a tooltip populated from `engagement-config.md` — 5.

```html
<div class="inflight-anchor" title="A1: Profitable Revenue Growth">Anchor: A1</div>
<div class="inflight-anchor" title="A2: Margin Expansion · A3: Working Capital Optimization">Anchor: A2, A3</div>
```

Multi-anchor cards concatenate names with ` · `. The strategic-anchor definition cards on the Why Now tab (where each anchor is fully defined) do NOT carry a tooltip on themselves — they ARE the definition.

---

## 16. Citation routing — visual behaviour

Body-text citation references (`[S#]`, `[B#]`, `[I#]`) switch to the destination tab AND scroll to the specific row. Each destination row carries `id="ref-S1"` / `id="ref-B3"` / `id="ref-I5"` for direct linking.

**CSS animation briefly highlights the destination row on arrival.**

See `structural-rules.md` — Citation routing for prefix definitions and tab routing.

---

## 17. Standard component templates

Engagement-specific values consumed from `engagement-config.md`. Render at Phase 9 from these templates rather than rebuilding each time.

### Glossary panel (Summary tab)

`<details open>` panel near the bottom of the Summary tab, expanded by default.

```html
<details open class="glossary-panel"
  style="margin: 32px 0 24px; padding: 20px 24px;
         background: var(--surface-2, #f6f7f9);
         border: 1px solid var(--rule, #e3e6ec);
         border-radius: 8px;">
  <summary>How to read this dashboard
    <span>— glossary of financial and AVP terms</span>
  </summary>
  <div class="glossary-grid">
    <div class="glossary-col">
      <h4>Financial terms</h4>
      <dl>
        <dt>P50 / P10–P90 / P&gt;90</dt>
        <dd>Percentile outcomes from the 10,000-trial Monte Carlo.
            P50 = median; P10–P90 = 80% confidence range;
            P&gt;90 = probability of clearing the hurdle.</dd>
        <!-- ... additional terms ... -->
      </dl>
    </div>
    <div class="glossary-col">
      <h4>AVP &amp; methodology</h4>
      <dl>
        <dt>AVP</dt>
        <dd>AI Value Platform — Slalom's framework for sizing and
            sequencing AI use cases against process tasks.</dd>
        <!-- ... additional terms ... -->
      </dl>
    </div>
  </div>
</details>
```

Token interpolation: `{wacc_pct}`, `{hurdle_rate_pct}`, `{industry composite}`, `{N}` from `engagement-config.md`. Add function-specific acronyms as additional `<dt>/<dd>` pairs when in scope.

### Methodology visual (Sources tab)

Seven horizontal phase cards replacing the legacy long-form methodology paragraph.

```html
<div class="methodology-grid"
  style="display: grid;
         grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
         gap: 8px; margin: 24px 0 32px;">
  <div class="methodology-card">
    <div class="methodology-phase">PHASE 1</div>
    <div class="methodology-title">Archetype synthesis</div>
    <div class="methodology-take">Peer 10-K patterns → {revenue_label} profile</div>
  </div>
  <!-- ... Phases 2–7 ... -->
</div>
```

### Gap-explanation paragraph (Assumptions tab)

Blue-bordered callout immediately after the Assumptions lead, before the I-rows table.

```html
<div class="gap-explanation">
  <strong>Why ${total_modeled} and not ${headline_high}?</strong>
  Big Four publications cite 25–40% productivity gains for AI in functional
  processes (e.g., 30–50% close-time reduction; 60–80% AP straight-through).
  Those are <em>process-level relative</em> gains. The portfolio modeled here
  converts those gains to dollars by multiplying the applicable cost base
  ({tech_spend_summary}, {headcount_summary}) by realistic per-process gains,
  then haircutting by adoption ramp and a {realization_factor} realization
  factor against industry composite — landing at ${total_modeled} run-rate,
  ~{rev_pct}% of ${revenue_label}. The 25–40% process gains are not lost;
  they're the mathematical input that lands here.
</div>
```

### Forcing-card structure (Why Now tab)

```html
<div class="forcing-card">
  <div class="forcing-title">{title — the bold claim}</div>
  <div class="forcing-tagline">{tagline — one sentence in plain English}</div>
  <p>{body — evidence, citations, sizing}</p>
</div>
```

See `editorial-rules.md` — Forcing-card tagline for content rules (every card must have title + tagline + body; QA verifies title-count == tagline-count).

### Phase 0 card (Roadmap tab)

Phase 0 cards never show `TBC`. Render with the engagement-specific dollar anchor:

```html
<div class="phase-card phase-0-card">
  <span class="phase-badge">Phase 0</span>
  <h3>Foundation</h3>
  <p class="muted small">
    Confirm data + platform readiness. Phase 0 has no direct benefit
    stream — it's the prerequisite for the rest. Sized as a shared
    {phase_0_anchor_label} platform investment, applied portfolio-wide
    (not double-counted per function).
  </p>
  <div class="phase-figs">
    <div class="phase-fig">
      <span class="lbl">UCs</span><strong>UCs N/A</strong>
    </div>
    <div class="phase-fig">
      <span class="lbl">One-time</span>
      <strong title="{phase_0_anchor_explainer}">{phase_0_anchor_label}</strong>
    </div>
    <div class="phase-fig">
      <span class="lbl">Run-rate</span><strong>—</strong>
    </div>
  </div>
</div>
```

Phase 3 backlog cards (zero phase-3 UCs) follow the same `UCs N/A` / `—` convention.

### Break-even callout (Roadmap tab)

Per `chart-conventions.md` — 4. A live, function-aware callout sits between the phasing-tab lead and the chart container, JS-synced with the function filter. The static fallback text uses the elapsed-month framing (`Year (be+1).M (month round((be+1)*12)) — portfolio`).

### Filter-sidebar prompt

```html
<p class="filter-sidebar-eyebrow">Filter by function</p>
<p class="filter-sidebar-prompt">
  Click any function below to focus every tab on that function&apos;s view.
  Click <strong>All Functions</strong> to return to the portfolio.
</p>
```

---

## 18. Bubble chart interaction

Every portfolio matrix on the AI Portfolio tab supports click interaction.

### Behaviour

1. **Click a bubble:** opens the UC modal AND filters the portfolio table to show only that UC's row. A "Show all use cases" reset button appears above the table.
2. **Click empty space on the chart:** resets the filter (equivalent to the reset button).
3. **Escape key:** closes the modal; does NOT reset the table filter (user may want to see the row after closing).

### Implementation pattern (canvas-based)

```javascript
// Store bubble positions during draw
var bubbleHits = [];
// During drawBubble():
bubbleHits.push({ id: d.id, cx: bx, cy: by, r: br });

// Click handler on canvas
canvas.addEventListener('click', function(e) {
  var rect = canvas.getBoundingClientRect();
  var scaleX = canvas.width / rect.width;
  var scaleY = canvas.height / rect.height;
  var mx = (e.clientX - rect.left) * scaleX;
  var my = (e.clientY - rect.top) * scaleY;
  // Hit detection: iterate bubbles in reverse (topmost first)
  for (var i = bubbleHits.length - 1; i >= 0; i--) {
    var h = bubbleHits[i];
    if ((mx-h.cx)*(mx-h.cx) + (my-h.cy)*(my-h.cy) <= h.r*h.r) {
      selectUC(h.id);  // filter table + open modal
      return;
    }
  }
  clearUCSelection();  // clicked empty space — reset
});
```

Add `cursor: pointer` to the canvas CSS when bubbles are present.

---

## 19. Dynamic chart redraw on function filter

When the function filter sidebar changes the active function, ALL charts must redraw with function-specific data — not just show/hide static content.

| Chart | All Functions view | Single function view |
|---|---|---|
| **Bubble chart** (AI Portfolio) | Shows all bubbles | Shows only that function's bubbles; Y-axis rescales |
| **Roadmap chart** (Roadmap tab) | Cumulative cost/benefit for full portfolio | Cumulative cost/benefit for that function only |

### Implementation pattern

Pre-compute per-function chart data and embed as a JavaScript lookup:

```javascript
var FP = {
  "all": { "cc": [71,101,...], "cb": [0,47,...] },
  "RCM": { "cc": [11,13,...], "cb": [0,6,...] },
  ...
};
```

Chart draw functions accept the current function as a parameter:

```javascript
function drawRoadmap(fn) {
  var d = FP[fn] || FP['all'];
  // ... draw using d.cc and d.cb
}
```

The `filterFn` handler calls both chart draw functions on every filter change. The `showTab` handler calls the relevant chart draw function when switching to a tab that has a chart, passing the current filter.

---

## 20. Tab panel CSS

```css
.panel { display: none; }
.panel.active { display: block; }
```

All tab content must be **inside its panel `<div>`** — orphan sections sitting between panels render in every PDF export.

---

## 21. Print / PDF fidelity

When a tab is exported as PDF, only the active tab's content should print:

1. All tab content must be **inside its panel `<div>`** — orphan sections that sit between panels render in every PDF export
2. CSS rule: `.panel { display: none } .panel.active { display: block }` (already specified above)
3. Optional `@media print { .panel:not(.active) { display: none !important } }` for safety
4. QA check (see `qa-checklist.md` — Panel placement): verify each tab's content is depth-1 inside its panel

**Symptom of orphaned content:** the same section appears in every tab's PDF export, despite being intended for one tab.

---

## 22. "Considered but cut" panel treatment

Below the active portfolio table on the AI Portfolio tab. Visual treatment: muted background. Rows are NOT clickable (no modals).

## "Evaluated but deprioritized" panel treatment

Below the "Considered but cut" panel (or below the active portfolio table if no cuts). Visual treatment: muted background — **distinct shade from "considered but cut"** (slightly warmer muted tone signalling "ready to activate" vs. "screened out"). Rows are NOT clickable.

The two panels are visually and semantically distinct:
- "Considered but cut" = lightweight record (ID, name, function, why cut)
- "Evaluated but deprioritized" = rich record (includes MC metrics, composite rank, reactivation note)

---

## 23. Strategic alignment layout patterns

### Pattern A — Equal-card grid (default for ≤4 anchors)

One card per strategic anchor in a uniform grid. Each card: anchor name, source citation(s), subtitle with specific target, UC count, aggregate value, 2–3 sentence description, mapped UC IDs.

### Pattern B — Thematic clustering (preferred for 5+ anchors)

Cluster anchors into 3 strategic themes:

```
[THEME 1 NAME ────────────── DRIVES UC-A · UC-B · UC-C · UC-D]
  [Anchor A1 mini-card]    [Anchor A2 mini-card]
[THEME 2 NAME ────────────── DRIVES UC-E · UC-F · UC-G]
  [Anchor A3 mini-card]    [Anchor A4 mini-card]
```

Theme names: 2–3 words articulating strategic posture. Each theme header carries the union of UC IDs. Anchor mini-cards are simplified: heading + citation, target line, stats (UCs · Annual value), single-line takeaway.

---

## 24. "How we sized this" section (per-UC modal)

The strongest credibility artefact in the modal.

### Visual structure

1. **Eyebrow:** `HOW WE SIZED THIS` (Slalom Blue)
2. **Formula:** human-readable calculation in italics
3. **Variable table:**

| Column | Content |
|---|---|
| Variable | Name, wrapped in CSS tooltip (`.vtt`) showing explanatory note |
| Value | The number used |
| Source | Color-coded tag: S# (green) = primary source, B# (blue) = benchmark, I# (amber) = inferred, Calculated (gray) = derived |

4. **Source legend:** *"S# = Primary source · B# = Benchmark · I# = Inferred estimate · Hover variable names for notes"* — each tag is itself a CSS tooltip hover target.

---

## 25. Monte Carlo confidence ranges (per-UC modal)

Three horizontal range bars (annual benefit, NPV, payback) with:
- Base ▼ marker
- P50 ● marker
- P10–P90 fill band

Plus a P(NPV>0) probability badge:
- Green: ≥95%
- Amber: 80–95%
- Red: <80%

---

## 26. Accessibility (WCAG 2.1 AA baseline)

The dashboard is an HTML artefact opened in browsers by C-suite readers, forwarded to compliance teams, and occasionally printed. Accessibility is both ethically required and practically necessary — a Slalom deliverable that fails basic screen-reader or keyboard tests reflects on the practice.

**Target: WCAG 2.1 AA.** AAA is aspirational; AA is the floor.

### Colour contrast

All text/background combinations must meet **4.5:1 for normal text** (≤18px regular, ≤14px bold) and **3:1 for large text** (>18px regular, >14px bold).

**Known palette risks — test and remediate:**

| Combination | Approximate ratio | Status | Remediation |
|---|---|---|---|
| White on `--slalom-blue` (#0C62FB) | ~3.5:1 | **Fails** normal text; passes large text | Use only for nav tab labels (14px bold = large text) and headings ≥18px. For body text on blue, use white on `--dark-blue` (#002FAF, ~7:1) instead |
| `--coral` (#FF4D5F) on white | ~3.2:1 | **Fails** normal text; passes large text | Use coral only for badges/pills with ≥14px bold text, or add a dark text color inside coral backgrounds. Never use coral as body-text color on white |
| `--muted` (#6b7588) on white | ~4.6:1 | **Passes** AA normal text (barely) | Acceptable for secondary text at ≥12px. Monitor — any lighter shade fails |
| `--teal` (#1BE1F2) on white | ~1.6:1 | **Fails** all sizes | Never use teal as text color on white. Use `--teal-deep` (#0e7a86, ~4.7:1) for teal-toned text |
| `--ink` (#0e1422) on `--bg` (#F6F8FB) | ~15:1 | Passes | Primary body text — no issues |
| White on `--dark-blue` (#002FAF) | ~7:1 | Passes | Hero text — no issues |
| `--pos` (#1f7a1f) on white | ~5.4:1 | Passes | Green probability badges — no issues |

**Rule:** before shipping, run a contrast check on every text/background pair that appears in the rendered HTML. Tools: Chrome DevTools color picker (shows ratio inline), or WebAIM Contrast Checker.

### Semantic HTML

- Use `<nav>` for the tab bar, `<main>` for the active panel content, `<section>` for major content sections, `<aside>` for the function-filter sidebar
- Use heading hierarchy (`h1` → `h2` → `h3`) without skipping levels. The dashboard title is `h1` (visually in the nav or hero); tab section titles are `h2`; sub-sections are `h3`
- Use `<table>` with `<thead>`, `<th scope="col">`, and `<th scope="row">` for all data tables — never `<div>` grids pretending to be tables
- Use `<button>` for tab buttons, filter buttons, and modal triggers — never `<div onclick>` or `<span onclick>`
- Use `<dialog>` or `role="dialog"` for modals (see — Focus management below)

### Keyboard navigation

- **Tab order** follows visual reading order (left-to-right, top-to-bottom within each panel)
- **Tab buttons** are focusable and activatable with Enter/Space. Arrow keys move between tabs (standard tab-list pattern)
- **Modal open/close:** Enter/Space opens the modal from a trigger; Escape closes it; Tab cycles through focusable elements inside the modal
- **Filter buttons** are focusable and activatable with Enter/Space
- **Chart bubbles** are not natively keyboard-accessible (canvas hit detection is pointer-only). Provide the sortable table as the keyboard-accessible equivalent — every UC reachable via the table row's click/Enter handler
- **Skip link:** add a visually hidden skip link at the top of the page: `<a href="#main-content" class="skip-link">Skip to content</a>` with CSS that shows it only on focus

```css
.skip-link {
  position: absolute; left: -9999px; top: auto;
  width: 1px; height: 1px; overflow: hidden;
}
.skip-link:focus {
  position: fixed; top: 8px; left: 8px; z-index: 9999;
  width: auto; height: auto; padding: 8px 16px;
  background: var(--dark-blue); color: #fff;
  border-radius: 4px; font-size: 14px;
}
```

### Focus management

- **Modal open:** on open, move focus to the modal's first focusable element (typically the close button or the first heading). Trap focus inside the modal while it's open — Tab at the last element wraps to the first; Shift+Tab at the first wraps to the last.
- **Modal close:** on close (Escape or close button), return focus to the trigger element that opened the modal (the table row or bubble chart trigger).
- **Tab switch:** on tab switch, move focus to the newly active panel's first heading or content element.

```javascript
// Focus trap pattern for modals
function trapFocus(modal) {
  const focusable = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0], last = focusable[focusable.length - 1];
  modal.addEventListener('keydown', function(e) {
    if (e.key !== 'Tab') return;
    if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
    else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
  });
  first.focus();
}
```

### ARIA attributes

- **Tab bar:** `role="tablist"` on the container; `role="tab"` + `aria-selected="true|false"` + `aria-controls="tab-{id}"` on each tab button; `role="tabpanel"` + `aria-labelledby="{tab-button-id}"` on each panel
- **Modals:** `role="dialog"` + `aria-modal="true"` + `aria-labelledby="{modal-title-id}"` on the modal container
- **Charts (canvas):** `role="img"` + `aria-label="{descriptive summary}"` on each `<canvas>`. The label should summarize the chart's key takeaway (e.g., "Scatter plot showing 12 use cases by annual benefit and relative level of effort. 8 cluster in the top-left quick-win quadrant.")
- **Tooltips:** the existing `.vtt` CSS tooltips are hover-only. Add `aria-describedby` linking the trigger to the tooltip `<span>` (give each tooltip an `id`), so screen readers announce the tooltip content when the trigger is focused
- **Live regions:** when the function filter updates chart data, use `aria-live="polite"` on the break-even callout and chart summary text so screen readers announce the change
- **Status pills:** use `role="status"` or a descriptive `aria-label` on in-flight status pills (e.g., `aria-label="Status: in production"`)

### Charts and data visualisation

Canvas-based charts are opaque to screen readers. For every chart, provide:

1. **`aria-label`** on the `<canvas>` element summarizing the chart takeaway
2. **A sortable table** as the accessible equivalent — the portfolio table on the AI Portfolio tab serves this role for the matrices; the phasing tab needs a small data table alongside the cumulative chart
3. **Visible axis labels and legends** (already specified in `chart-conventions.md`) — these help low-vision users who can see the chart but not fine details

### Images

- **AVP Analysis value-chain images:** add `alt` text describing the visualization (e.g., "Value-chain heatmap for Revenue Cycle Management showing 47 L3 tasks color-coded by AI readiness, ranging from 42% to 91%"). The alt text should convey what the image communicates, not describe every pixel.
- **Slalom logo:** the inline SVG in the nav should carry `role="img"` + `aria-label="Slalom"` on the `<svg>` element
- **Decorative elements:** arrows between scope-waterfall nodes, accent borders, gradient backgrounds — use `aria-hidden="true"` to keep screen readers from announcing them

### Reduced motion

Respect the user's motion preferences for the citation-highlight animation and any hover transitions:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Print accessibility

The existing print rules (see 21) ensure only the active tab prints. Additionally:
- Ensure all text prints in high contrast (no light-grey-on-white that's legible on screen but invisible on paper)
- Citation links should print their URL or reference ID visibly (they're not clickable on paper)
- Charts should be sized to fit the print width without cropping

### QA checklist additions

Add these checks to `qa-checklist.md` in a future pass:

- [ ] Every `<canvas>` has `role="img"` + `aria-label`
- [ ] Tab bar uses `role="tablist"` / `role="tab"` / `role="tabpanel"` pattern
- [ ] Modals use `role="dialog"` + `aria-modal="true"` + focus trap
- [ ] No `<div onclick>` or `<span onclick>` — interactive elements are `<button>` or `<a>`
- [ ] Skip link present and visible on focus
- [ ] All data tables use `<th scope>` headers
- [ ] Slalom logo SVG has `role="img"` + `aria-label="Slalom"`
- [ ] `@media (prefers-reduced-motion)` rule present
- [ ] Contrast check passes on all text/background pairs (4.5:1 normal, 3:1 large)
- [ ] AVP Analysis images have descriptive `alt` text

---

## 28. Visual anti-patterns

| Pattern | Why it reads as AI-assembled |
|---|---|
| Eyebrow + title with same text | Repetition that adds no information |
| 6 equal cards in a 3×2 grid | Catalog feel; humans group |
| Half-step type sizes (12.5, 13.5) | Cumulative inconsistency invisible per element but obvious in aggregate |
| Multiple gradient backgrounds | Decorative, not functional |
| Every section has different background | Chrome-heavy; whitespace beats backgrounds |
| Pills inside pills inside cards | Visual noise that doesn't earn its space |
| Caps within sentence-case headings | "Demonstrate Early Value" inside otherwise sentence-case section is a tell |
| Coloured top-borders on every card | Makes everything look like a status indicator |
| Multiple shadow stacking on one element | Over-decorated |
| Forced symmetry where reality is uneven | If you have 7 anchors, don't pretend you have 6 |

---

## Quick cheat sheet

```
Palette:       CSS vars only; brand + accent + neutrals
Type scale:    ≤9 sizes (10/11/12/13/14/18/22/28 + ≤3 hero display)
Cards:         ≤2 base patterns (standard/compact), 8px radius, 4-base padding
Spacing:       4-base scale (4/8/12/16/24/32/48), section padding 48px
Chrome:        Minimise — gradients only on hero, single accent per card type
Tooltips:      CSS .vtt component — never native title for interactive content
Charts:        Explicit px height parent div; 480px for matrices, 360px for others
Modals:        max-width 1000px, max-height 88vh, scrollable, focus-trapped
Print:         All tab content inside its panel div; @media print safety rule
Interaction:   Bubble click → modal + table filter; function filter → redraw all charts
Accessibility: WCAG 2.1 AA floor; semantic HTML; keyboard nav; ARIA on tabs/modals/charts;
               contrast-check all palette combos; skip link; prefers-reduced-motion
```
