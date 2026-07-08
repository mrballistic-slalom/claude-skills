# Skeleton Transformer Guide — v3.2

**Companion to `references/build-skeleton.html` — read this BEFORE filling any placeholders.**

## v3.2 additions you must know about

- **Per-UC math validation** — `set_engagement_data()` rejects builds where the per-UC numbers violate sanity bounds (NPV/benefit ratio outside [1.2, 2.6]×, payback under 3 months or over 60, IRR outside [0%, 250%], invest under $0.2M). Catches the v3.1 cross-environment variance where claude.ai and Claude Code produced 169% different portfolio NPVs from identical inputs.
- **UC ID format pinned** — all UC IDs must match `UC-NN` (two-digit zero-padded). `UC-001` or `UC-1` is rejected.
- **Filename convention enforced** — `Skeleton.write()` requires the output filename match `YYYYMMDD - Slalom AI PoV - <Client> - DRAFT v<#>.html`. Use `Skeleton.next_output_path(client_name, output_dir)` to auto-generate a versioned path that never overwrites prior versions.
- **`meta.big_one_type`** — optional field on the engagement data dict; one of `5yr_npv` / `annual_benefit` / `payback`. Pin this per audience: CFO/board → `5yr_npv`, COO/Ops → `annual_benefit`.

## v3.4 additions — sidebar filters recompute numbers too

`_applyFilters()` now calls `_recomputeAggregates()` at the end, which updates aggregated values across Summary / AI Portfolio / Roadmap tabs based on the currently-filtered UC set.

For this to work, Phase 9 build must include **canonical IDs** on the specific value elements:

**Hero block (Summary tab) — when filling `fill_section('HERO', ...)`:**

```html
<div class="hero-bigone" id="hero-bigone-val">$332M/yr</div>

<div class="kpi-strip">
  <div class="kpi-row-label">What it delivers</div>
  <div class="kpi"><div class="lbl">Annual benefit</div>
    <div class="val" id="hero-kpi-r1-c1-val">$332M</div><div class="sub">* P50</div></div>
  <div class="kpi"><div class="lbl">5-yr NPV</div>
    <div class="val" id="hero-kpi-r1-c2-val">$612M</div><div class="sub">* 65% real.</div></div>
  <div class="kpi"><div class="lbl">Portfolio scope</div>
    <div class="val" id="hero-kpi-r1-c3-val">15 UCs</div><div class="sub">6 functions</div></div>

  <div class="kpi-row-label">What it costs</div>
  <div class="kpi"><div class="lbl">Total investment</div>
    <div class="val" id="hero-kpi-r2-c1-val">$54M</div><div class="sub">* one-time</div></div>
  <div class="kpi"><div class="lbl">Avg payback</div>
    <div class="val" id="hero-kpi-r2-c2-val">10 mo</div><div class="sub">* sample-weighted</div></div>
  <div class="kpi"><div class="lbl">Annual run cost</div>
    <div class="val" id="hero-kpi-r2-c3-val">$11M/yr</div><div class="sub">* sustained</div></div>
</div>
```

**AI Portfolio header (Portfolio Overview band):**

```html
<div class="ap-stat-strip">
  <div class="ap-stat"><div class="ap-stat-val">50</div><div class="ap-stat-lbl">Evaluated</div></div>
  <div class="ap-stat-div"></div>
  <div class="ap-stat"><div class="ap-stat-val" id="ap-stat-prio-count">15</div>
    <div class="ap-stat-lbl">Prioritized</div></div>
  <div class="ap-stat-div"></div>
  <div class="ap-stat"><div class="ap-stat-val" id="ap-stat-annual-benefit">$332M</div>
    <div class="ap-stat-lbl">Annual Benefit</div></div>
  <div class="ap-stat-div"></div>
  <div class="ap-stat"><div class="ap-stat-val" id="ap-stat-npv">$612M</div>
    <div class="ap-stat-lbl">5-yr NPV</div></div>
</div>
```

**Filter status indicator (visible across all tabs — put it once in the persistent disclaimer area or near the top of the page):**

```html
<div id="filter-status" class="filter-status-badge" style="display:none"></div>
```

Add CSS (already in the v3.4 skeleton) styles `.filter-status-badge` as a yellow pill that only displays when a filter is active.

**Roadmap break-even chart** auto-recomputes via `_computeFilteredRoadmap()` — no IDs needed. The JS rebuilds the cumulative-benefit and cumulative-cost arrays from filtered UCs using a default phase-based ramp (P_N deploy in Y_N at 50%, 100% Y_N+1, etc.) and applies the engagement's `meta.realization` and `meta.tax_rate` for haircuts.

**Elements without these IDs simply skip the recompute** — no errors, just no filter-aware update for that element. This is graceful degradation: if Claude's fill_section forgot an ID, the build still ships, just with a stale value on that one element when the user filters.

---

## v3.3 additions (sidebar filters now work on every tab)

- **Cross-tab filtering** — `_applyFilters()` now applies the View / Function / Strategic Goal filters across every tab, not just AI Portfolio. Any card carrying `data-fn` and/or `data-goal` attributes participates.

Card types that participate in cross-tab filtering (Phase 9 build must populate `data-fn` and/or `data-goal` where applicable):

| Card type | Tab | Filter dimension |
|---|---|---|
| `.uc-item` (tiles + table rows) | AI Portfolio + Assumptions | View + Function + Goal |
| `.anchor-card` | Why Now (Strategic Alignment) | Goal |
| `.mkttrend-card` | Why Now (Market Trends) | Goal (occasionally Function) |
| `.competitor-card` | Why Now (Competitor moves) | Goal |
| `.forcing-card` | Why Now (Forcing functions) | Goal |
| `.inflight-card` | Why Now (In-flight initiatives) | Function (sometimes Goal) |
| `.avp-gallery-item` | AVP Analysis | Function |
| `.phase-card` | Roadmap | Phase (Goal optional) |
| `.src-card` | Sources | Function + Goal (whichever UCs the source supports) |

**Cards without `data-fn` AND without `data-goal` are treated as universal** — always visible regardless of filter state. Use this for cross-cutting content (Phase 0 cards, methodology citations, ambient sources).

Example HTML when filling sections:

```html
<!-- Filterable: anchor card tied to "Margin Expansion" goal -->
<div class="anchor-card" data-goal="Margin Expansion">...</div>

<!-- Filterable: source supporting UCs in Supply Chain Ops -->
<div class="src-card" data-fn="Supply Chain Ops" data-goal="Margin Expansion">...</div>

<!-- Universal: methodology citation visible on every filter -->
<div class="src-card">...</div>
```

## What changed in v3.0

v3.0 inverts the build model. Previous skeletons had `{{}}` markers around every variable element; Claude filled each one. v3.0 introduces a **data-driven** skeleton:

- **The skeleton renders itself from a single JSON block.** UC tiles, table rows, matrix bubbles, and Assumptions table rows are all generated by JavaScript at page load from `<script id="portfolio-data">`. The skeleton's HTML for these areas is empty containers; JS populates them at `DOMContentLoaded`.
- **UC count is flexible.** Engagement data with 6 UCs, 14 UCs, 25 UCs — all render with no skeleton mutation.
- **Matrix bubble positions live in data, not HTML.** Each UC carries `matrices: { "benefit-loe": {x, y, size}, ... }`. The skeleton has zero hardcoded positions.
- **Only the hero + a small set of inline placeholders remain as `{{}}` markers.** Everything else either flows through the JSON block or is narrative copy you customize via the Edit tool.

## Two paths, one contract

### Path 1 — Claude.ai (no shell): use `references/transform.py`

```python
import sys; sys.path.insert(0, 'references')
from transform import Skeleton

sk = Skeleton('references/build-skeleton.html')

# Step A — engagement data JSON block (the single source for all UC content)
# Per-UC math is validated here; build fails fast if numbers are outside sanity bounds.
sk.set_engagement_data(engagement_data_dict)

# Step B — inline placeholders (top-level identifiers).
# Note: CLIENT_NAME runs LAST among the inlines. If you want narrative customization
# that references {{CLIENT_NAME}}, do those via fill_section BEFORE this step.
sk.fill_inline('PAGE_TITLE', 'Client — AI Portfolio | Slalom')
sk.fill_inline('NAV_TITLE', 'Client · AI Transformation PoV · May 2026')
sk.fill_inline('CLIENT_NAME', 'Client Name')          # appears 19× in narrative
sk.fill_inline('ENGAGEMENT_DOMAIN', 'Industry/Domain')

# Step C — narrative sections (REQUIRED — write() refuses if any unfilled)
sk.fill_section('HERO', hero_html)
sk.fill_section('ANCHOR_CARDS', anchor_cards_html)
sk.fill_section('MARKET_TRENDS', market_trends_html)
sk.fill_section('COMPETITORS', competitor_cards_html)
sk.fill_section('FORCING_FUNCTIONS', forcing_function_cards_html)
sk.fill_section('AVP_PROCESS_STRIP', avp_process_strip_html)
sk.fill_section('AVP_VALUE_CHAIN', avp_gallery_items_html)
sk.fill_section('SOURCES', source_cards_html)

# Step D — get the next canonical output path (never overwrites prior versions)
out_path = Skeleton.next_output_path('Dollar Tree',
    '/Users/aaron.butler/claude-workspace/projects/Dollar Tree/')
# → '/Users/.../Dollar Tree/20260528 - Slalom AI PoV - Dollar Tree - DRAFT v1.html'
# (or v2/v3/… if prior versions exist for the same client + date)

# Step E — write (validates the full contract; raises on any violation)
sk.write(out_path)
```

`Skeleton.write()` refuses to write if:
- Any `{{PLACEHOLDER}}` is unfilled
- Any required section (`HERO`, `ANCHOR_CARDS`, `MARKET_TRENDS`, `COMPETITORS`, `FORCING_FUNCTIONS`, `AVP_PROCESS_STRIP`, `AVP_VALUE_CHAIN`, `SOURCES`) was not filled via `fill_section`
- `set_engagement_data()` was never called
- Any filter chip (`.filter-btn`, `.if-chip`, `.aim-filter-chip`, `.func-filter-chip`) is wrapped in `<!-- -->`
- A `portfolio-toggle-suppressed` or `view-toggle-suppressed` comment exists
- Output line count exceeds 1.8× skeleton (generation canary — v3.0 expects ratio ~1.0×)
- **(v3.2)** Output filename does not match `YYYYMMDD - Slalom AI PoV - <Client> - DRAFT v<#>.html`
- **(v3.2)** Output file already exists at that path (never overwrites — use `next_output_path()`)

`Skeleton.set_engagement_data()` refuses to inject data if:
- **(v3.2)** Any UC ID is not `UC-NN` (two-digit zero-padded)
- **(v3.2)** Any UC has missing `benefitNum`/`npvNum`/`investNum`/`paybackNum`
- **(v3.2)** Any UC has NPV/benefit ratio outside `[1.2, 2.6]×` — guards against the 1.0× compression (claude.ai v3.1) and 2.8×+ inflation failure modes
- **(v3.2)** Any UC has `paybackNum < 3` months or `> 60` months
- **(v3.2)** Any UC has `irrNum > 250%` (model-output cap artifact) or `< 0%`
- **(v3.2)** Any UC has `investNum < $0.2M` (too small for a platform build)
- **(v3.2)** Any UC's benefit exceeds 1% of engagement revenue (when `meta.revenue_M` is set)

### Path 2 — Claude Code (has shell): cp + Edit tool

```bash
cp references/build-skeleton.html output/{slug}_AI_Portfolio_v1.html
```

Then use the `Edit` tool:
- Replace `{{ENGAGEMENT_DATA_JSON}}` with the serialized engagement data dict
- Replace each remaining `{{PLACEHOLDER}}` with engagement content
- Customize narrative copy in place (the skeleton ships with Acme/Manufacturing sample content as design reference; replace it with engagement-specific text)

After editing, run `python3 references/qa-automated-checks.py output/...html --client-hq=US` to verify.

## Engagement data shape

```python
engagement_data = {
    "meta": {                                # (v3.2) engagement-level metadata
        "client": "Dollar Tree",
        "revenue_M": 19400,                  # revenue in $M — feeds per-UC benefit ceiling check
        "big_one_type": "5yr_npv",           # "5yr_npv" | "annual_benefit" | "payback"
        "realization": 0.65,                 # exact value, not a range
        "hurdle_rate": 0.11,                 # exact value
        "tax_rate": 0.24,                    # exact value
        "wacc": 0.085,                       # exact value
        "horizon_years": 5
    },
    "ucs": {
        "UC-01": {                            # MUST match pattern UC-NN (two-digit)
            # Identification
            "name": "Demand Forecasting & Inventory Optimization",
            "fn": "Supply Chain Ops",        # used for filter + tag display
            "goal": "Margin Expansion",      # strategic goal / anchor name
            "loe": "Quick Win",              # display label: "Quick Win" / "Standard" / "Major investment"
            "loeClass": "qw",                # CSS modifier: "qw" / "std" / "mi"
            "phase": "Phase 1",              # "Phase 1" / "Phase 2" / "Phase 3" / "Deprioritized"
            "pool": "prio",                  # "prio" (recommended portfolio) or "all" (evaluated only)

            # Narrative
            "desc": "ML-driven demand signals replace static reorder rules...",

            # Display strings (rendered as-is in tiles/tables)
            "benefit": "$4.2M",
            "npv": "$7.5M",                   # ≈ 1.8× annual for 5yr horizon at 65% realization
            "payback": "14 mo",               # ≥ 3 months (sanity floor)

            # Numeric values (validated against UC_MATH_BOUNDS in v3.2)
            "benefitNum": 4.2,                 # annual benefit in $M
            "npvNum": 7.5,                     # 5-yr NPV; must be 1.2× to 2.6× of benefitNum
            "paybackNum": 14,                  # months; must be 3 to 60
            "irrNum": 58,                      # IRR %; must be 0 to 250
            "investNum": 1.2,                  # implementation $M; must be ≥ 0.2

            # Matrix bubble positions (one entry per matrix view ID in the skeleton)
            "matrices": {
                "benefit-loe":  {"x": 25, "y": 20, "size": 44},
                "npv-payback":  {"x": 30, "y": 18, "size": 38},
                "irr-payback":  {"x": 30, "y": 16, "size": 34}
                # "strategic" matrix is rendered as a placeholder; bubbles optional
            }
        },
        "UC-02": { ... },
        # ... one entry per use case in the engagement
    },
    "roadmap": {                              # required for _renderRoadmapChart()
        "benefit": [0, 2, 8, 22, 41, 60],
        "cost":    [0, -3, -10, -11, -13, -15],
        "yScaleMax": 65, "yScaleMin": -15,
        "yTicks":   [60, 40, 20, 0, -10],
        "yearLabels": ["Year 0","Year 1","Year 2","Year 3","Year 4","Year 5"],
        "phaseBands": [
            {"x":70,"w":37,"fill":"var(--tint-blue-bg)","opacity":0.55,"label":"PH 0"},
            {"x":107,"w":113,"fill":"var(--tint-blue-bg)","opacity":0.45,"label":"PHASE 1","divider":True},
            {"x":220,"w":150,"fill":"var(--tint-amber-bg)","opacity":0.5,"label":"PHASE 2","divider":True},
            {"x":370,"w":450,"fill":"var(--tint-green-bg)","opacity":0.6,"label":"PHASE 3+","divider":True}
        ],
        "breakEven": {"x":390, "y":172, "monthLabel":"~month 26"}
    }
}
```

### Math validation reference (v3.2)

`set_engagement_data()` runs `_validate_uc_math()` which checks every UC against `Skeleton.UC_MATH_BOUNDS`:

| Field | Min | Max | Rationale |
|---|---|---|---|
| `npvNum / benefitNum` | 1.2× | 2.6× | At 5yr horizon, 65% realization, 24% tax, 11% hurdle: expected ≈ 1.85×. Range [1.2, 2.6] absorbs legitimate parameter variance (60–75% realization, 8–12% hurdle). |
| `paybackNum` | 3 mo | 60 mo | <3 months ignores realization haircut + ramp; >60 means UC shouldn't be in portfolio. |
| `irrNum` | 0% | 250% | <0% means UC shouldn't be in portfolio; >250% is a cap artifact. |
| `investNum` | $0.2M | (n/a) | <$0.2M is too small for a platform deployment (coding task, not engagement). |
| `benefitNum / revenue_M` | (n/a) | 1.0% | A single UC shouldn't capture >1% of company revenue. Engagement-level sanity check (requires `meta.revenue_M`). |

If your model produces values outside these bounds, the build fails fast. Either fix the methodology or override `Skeleton.UC_MATH_BOUNDS` before calling `set_engagement_data()` (use sparingly; document the override in the decisions log).

**Matrix view keys** correspond to the skeleton's `.matrix-view` elements' `id` attributes with the `matrix-` prefix stripped:

| Skeleton element ID | Use in data `matrices` map |
|---|---|
| `id="matrix-benefit-loe"` | `"benefit-loe"` |
| `id="matrix-npv-payback"` | `"npv-payback"` |
| `id="matrix-strategic"` | `"strategic"` (optional) |
| `id="matrix-irr-payback"` | `"irr-payback"` |

The skeleton's `_renderMatrixBubbles()` JS function iterates each `.matrix-view`, looks up that view's UCs in the data, and places each as a positioned `.matrix-bubble`. UCs with no entry for a given matrix simply don't appear in that view.

## What renders from data automatically

When `set_engagement_data()` provides a `ucs` dict, the following render at page load with **zero** additional skeleton HTML:

- **UC tile cards** in the AI Portfolio tab — `_renderUCTiles()`
- **UC table rows** in the AI Portfolio tab — `_renderUCTableRows()`
- **Assumptions table rows** in the Assumptions tab — `_renderAssumpTable()`
- **Matrix bubbles** in every `.matrix-view` — `_renderMatrixBubbles()`

JS update functions in the skeleton (`_recomputePortfolio`, `_updateTotals`, `_applyFilters`, `sortTable`, etc.) all read from `ucData` / DOM elements with the standard `pf-{id}-{field}` and `tb-{id}-{field}` and `arow-{id}-{field}` ID patterns — these IDs are generated by the renderers and the existing JS continues to work unchanged.

## What you customize manually

The skeleton ships with **Acme Industries / Manufacturing & Operations** sample narrative inline (it served as the v16 design reference). For an engagement, you customize:

1. **Hero block** — via `fill_section('HERO', html)`. Pass the hero's inner HTML (everything between `<!-- {{HERO_START}} -->` and `<!-- {{HERO_END}} -->`). Include hero-eyebrow, hero-title, hero-tagline, hero-bigone, hero-bigone-sub, kpi-strip, phase-strip, hero-caveat as appropriate.

2. **Top-level identifiers** — via `fill_inline`:
   - `PAGE_TITLE` — browser tab title
   - `NAV_TITLE` — nav bar h1 (e.g. "Dollar Tree · AI Transformation PoV · May 2026")
   - `CLIENT_NAME` — appears 19× across the narrative; substituted everywhere via single `fill_inline` call
   - `ENGAGEMENT_DOMAIN` — short domain descriptor (e.g. "Mass Merchandise / Discount Variety")

3. **Narrative content (Acme sample)** — these areas ship with Acme/Manufacturing-specific text that should be customized for the engagement. Customize via the `Edit` tool (Claude Code) or post-`write()` `html.replace` operations. The sections involved:
   - **Why Now tab** — anchor cards (8 cards, sample maps to manufacturing anchors), market trends section, competitor section, AI success patterns
   - **AVP Analysis tab** — value chain dimensions and process strips (sample maps to manufacturing functions)
   - **Roadmap tab** — phase card narratives, callout-strip context
   - **Assumptions tab** — model note, gap-card text
   - **Sources tab** — source citations and "used for" mappings

Each of these is intentionally NOT a `{{}}` placeholder so you can write engagement-fit prose with full HTML formatting freedom. The skeleton's QA script flags client-language violations (competitor names, British spellings, emoji badges, etc.) on the final output.

## CSS class canon (v16 — large surface)

The skeleton's `<style>` block defines ~150 classes. Critical families:

| Family | Example classes |
|---|---|
| Nav / header | `.nav`, `.nav-inner`, `.nav-left`, `.nav-logo-wrap`, `.nav-title`, `.tab-btns`, `.tab-btn` (+ `.active`) |
| Sidebar | `.sidebar`, `.sidebar-inner`, `.filter-label`, `.filter-btn`, `.fb-icon`, `.fb-label`, `.fb-text`, `.fb-count`, `.fb-swatch`, `.sidebar-sep` |
| Hero | `.hero`, `.hero-inner`, `.hero-eyebrow`, `.hero-title` (+ `<span>`), `.hero-tagline`, `.hero-bigone`, `.hero-bigone-sub`, `.kpi-strip`, `.kpi-row-label`, `.kpi` (+ `.lbl` / `.val` / `.sub`), `.phase-strip`, `.phase-pip` (chevron-shaped via clip-path), `.hero-caveat` |
| Tab panels | `.tab-panel` (+ `.active`), `.disclaimer`, `.tab-h2`, `.tab-sub`, `.page` |
| Anchor cards (Why Now) | `.anchor-grid`, `.anchor-card`, `.anchor-code`, `.anchor-icon`, `.anchor-name`, `.anchor-source`, `.anchor-uc` |
| Market trends | `.mkttrend-grid`, `.mkttrend-card`, `.mkttrend-implication` |
| Competitor section | `.competitor-grid`, `.competitor-card`, `.competitor-gap` |
| AI Portfolio header | `.ap-outer`, `.ap-summary`, `.ap-summary-text`, `.ap-section`, `.ap-section-label`, `.ap-stat-strip`, `.ap-stat`, `.ap-stat-val`, `.ap-stat-lbl`, `.ap-stat-div` |
| Lens / matrix selector | `.lens-tabs`, `.lens-tab` (+ `.active`), `.matrix-view` (+ `id="matrix-XXX"`), `.matrix-plot`, `.matrix-plot-row`, `.matrix-y-label`, `.matrix-x-label`, `.matrix-legend`, `.matrix-bubble`, `.matrix-placeholder-msg` |
| UC tiles | `.uc-tiles`, `.uc-tile` (+ `.uc-item`), `.uc-tile-header`, `.uc-id`, `.uc-phase`, `.uc-select-btn` (+ `.selected`), `.uc-tile-name`, `.uc-tile-tags`, `.uc-tag` (+ `.uc-tag-fn` / `.uc-tag-goal` / `.uc-tag-loe-qw` / `.uc-tag-loe-std` / `.uc-tag-loe-mi`), `.uc-tile-desc`, `.uc-tile-metrics`, `.uc-metric-val`, `.uc-metric-lbl` |
| UC table | `.uc-table-wrap`, `.uc-table`, `.sortable`, `[data-col]` |
| AVP analysis | `.avp-outer`, `.avp-gallery`, `.avp-gallery-item`, `.avp-gallery-img`, `.avp-gallery-ph`, `.avp-gallery-ph-lbl`, `.avp-gallery-caption`, `.avp-gallery-caption-title`, `.avp-gallery-caption-desc`, `.avp-process-strip`, `.avp-step`, `.avp-step-num`, `.avp-step-label`, `.avp-step-desc`, `.avp-dim-grid`, `.avp-dim-pill`, `.avp-dim-num`, `.avp-dim-name`, `.avp-dim-desc` |
| Roadmap | `.roadmap-views`, `.roadmap-view`, `.roadmap-cost-table` |
| Assumptions sliders | `.assump-params-grid`, `.assump-param-card`, `.assump-param-label`, `.assump-param-value`, `.assump-param-range`, `.assump-param-note`, `.assump-slider`, `.assump-reset-btn`, `.assump-static-grid`, `.assump-static-card`, `.assump-model-note` |
| Assumptions impact | `.assump-impact-grid`, `.assump-impact-card`, `.assump-impact-header`, `.assump-impact-title`, `.assump-impact-label`, `.assump-impact-value`, `.assump-impact-delta` (+ `.pos` / `.neg`), `.assump-delta-pos`, `.assump-delta-neg` |
| Assumptions UC table | `.assump-uc-table`, `.assump-uc-id`, `.assump-uc-nm`, `.assump-deprio` |
| Sources | `.src-grid`, `.src-card`, `.src-visible`, `.src-card-header`, `.src-chip-type`, `.src-chip-slalom`, `.src-chip-client`, `.src-citation`, `.src-used-for`, `.src-uc-row`, `.src-uc-row-lbl`, `.src-uc-tag`, `.src-scaffold-note`, `[data-src-type]` |
| Disclaimer | `.disclaimer` (single instance, persistent across tabs) |

Do not invent variants. If a class isn't defined in the skeleton, either use the canonical name or add the rule to the skeleton's `<style>` block before using it.

## JS function inventory

The skeleton ships ~30 JS functions. All call sites and IDs they read/write are documented inline. Major:

| Function | What it does |
|---|---|
| `showTab(id)` | Tab switching |
| `setView('prio'|'all', btn)` | Portfolio view toggle (Prioritized ↔ All Evaluated) |
| `setFn(fnName, btn)` | Function filter |
| `setGoal(goalName, btn)` | Strategic goal filter |
| `setMatrix(name, btn)` | Matrix lens selector |
| `setListView('tiles'|'table', btn)` | Toggle tile vs table view |
| `setRoadmapView(view, btn)` | Roadmap 5-view toggle |
| `setSrcFilter(type, btn)` | Source filter |
| `sortTable(col)` | Sort UC table by column |
| `toggleSelect(id)` | Add/remove UC from `_selected` set |
| `highlightUC(id)` / `clearHighlight()` | Hover highlight cross-element |
| `showBubbleTip(el, id)` / `hideBubbleTip()` | Matrix bubble tooltip |
| `_updateParam(key, val)` | Slider param update (WACC, FTE cost, adoption, impl buffer) |
| `_resetParams()` | Reset Assumptions sliders to defaults |
| `_recomputePortfolio()` | Recalculate UC metrics from slider params |
| `_computeUCMetrics(uc, params)` | Per-UC DCF calculation |
| `_renderUCTiles()` / `_renderUCTableRows()` / `_renderAssumpTable()` / `_renderMatrixBubbles()` | v3.0 data-driven renderers |
| `_initFromData()` | Wraps all renderers + base-case recompute |

## QA after writing

`Skeleton.write()` runs structural checks. After it succeeds, run the content/style QA:

```bash
python3 references/qa-automated-checks.py output/{slug}_AI_Portfolio_v1.html --client-hq=US
```

Exit code 0 required for delivery.
