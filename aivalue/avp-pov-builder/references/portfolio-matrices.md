# Portfolio Matrices

Matrices are the AI Portfolio tab's storytelling spine. Every PoV ships **at least one** matrix on the AI Portfolio tab; up to **five** when the audience and data warrant it. The skill recommends a shortlist; the user decides which render.

This doc owns:

1. The catalogue of axis pairs and when each tells the right story
2. The relative LOE percentile (computation, rationale capture, deep-dive tile rendering)
3. Audience → matrix shortlist mapping
4. Selection timing (after Phase 6 MC) and recommendation logic
5. Rendering rules — title, subtitle takeaways, classification overlay, deprioritized treatment, bubble sizing, axis convention

---

## When matrix selection happens

**Phase 6.5 — Matrix selection.** Runs after Phase 6 (Monte Carlo on the full broad pool) and before Phase 7 downselection. MC outputs feed the recommendation logic — some axis pairs go dead if the underlying dimension doesn't discriminate (e.g., every candidate paying back in 14–18 months kills "Break-Even" as an axis), and only MC tells you that.

The selection step itself is fast: skill recommends 1–3 matrices from the catalogue based on audience + intent + which dimensions discriminate, user picks (or adds, up to the cap of 5), skill renders.

---

## The relative LOE percentile

### Why a new measure

Existing LOE tier (Quick Win / Standard Project / Major Initiative) is a categorical classifier that feeds ramp curves and compute surcharges in `financial-model.md`. It is **kept as-is** for those purposes.

Matrices need a continuous, relative measure — three tiers collapse 50 candidates into three columns and kill chart discrimination. The relative LOE percentile is computed per bundle and used **only on matrix axes and in the deep-dive tile**.

### Composition

Compute a per-bundle relative LOE score from the following inputs, drawn from the AVP feature-level signals plus bundle-level reasoning:

| Component | Source | Contribution |
|---|---|---|
| **Implementation cost** | Phase 5 financial sizing (one-time investment) | Higher cost → higher LOE |
| **Change burden** | Bundle reasoning: roles affected, process redesign depth, training scope, org-design implications | More change → higher LOE |
| **Tech maturity** | Feature-level `technologies` field aggregated to bundle. Mature/proven (RAG, classification, supervised forecasting) → low; frontier (multi-agent orchestration, novel multimodal, autonomous decisioning) → high | More frontier → higher LOE |
| **Data readiness** | Average `data_readiness` signal from constituent AVP features (or inferred from Task Analysis if missing) | Lower readiness → higher LOE |
| **Regulatory / org friction** | Bundle reasoning: regulated domain (healthcare, financial services compliance), union/works-council exposure, customer-facing risk | More friction → higher LOE |

The five components are not equally weighted. Default weights:

- Implementation cost: 30%
- Change burden: 25%
- Tech maturity: 20%
- Data readiness: 15%
- Regulatory / org friction: 10%

Override only when the engagement has a specific reason (e.g., heavily regulated client → bump regulatory friction to 25%, drop change burden to 20%). Document any override in the Assumptions tab.

### Scale — relative percentile across the broad pool

LOE is reported as a **0–100 percentile across the ~50-candidate broad pool**, not an absolute score. Lowest aggregate LOE = 0, highest = 100, ranks linearly between.

Why percentile, not 1–5 ordinal: discrimination. With 50 candidates, a 1–5 ordinal collapses 10 candidates per bin and clusters everything on the chart. Percentile preserves separation and lets the audience see which bundles are *relatively* easier or harder.

**Read as relative, not absolute.** The axis label must say *"Relative LOE — lower = easier (vs. broad pool)"* so the audience doesn't read it as absolute hours or dollars. Two clients' LOE percentiles are not comparable across engagements.

### Axis convention — natural orientation, labeled win quadrant

**Axes follow natural orientation, not forced inversion.** Lower numbers sit on the left (X) and at the bottom (Y); higher numbers sit on the right and top. So short break-even goes left, low LOE goes left, low cost goes down — exactly as a reader expects.

**The win quadrant therefore varies by matrix.** When "more = good" on both axes (e.g., Strategic Anchor × Annual Benefit), the win is top-right. When Y is "more = good" and X is "less = good" (e.g., Annual Benefit × Relative LOE, where short LOE is the win), the win is **top-left**. Each catalogue entry below states its win quadrant explicitly.

**Every matrix labels its win quadrant** in the chart background (faint grey, 11px, e.g., *"Quick wins"* in the top-left of an Annual Benefit × LOE chart). The audience reads the chart fastest when the win corner is named, regardless of which corner it is.

### Rationale + assumptions in the deep-dive tile

**Mandatory.** Every per-UC modal (per `structural-rules.md` — Per-UC modal) carries an LOE rationale block in Section 9 (or as an extension of it — see `structural-rules.md` — LOE rationale block).

The block contains:

- **Headline:** *"Relative LOE: [N] / 100 ([percentile descriptor — e.g., easier than 73% of the broad pool])"*
- **Component breakdown table:** Component · Score · Weight · Contribution
- **Reasoning paragraph (≤120 words):** Why this bundle scores where it does on each component. Reference the AVP feature evidence for tech maturity and data readiness; reference the bundle's process scope for change burden; reference any regulatory anchor for friction.
- **Key assumptions (bullet list, ≤5 items):** What had to be assumed to compute the score. Tag each `[I#]` if material to the modeled output.

The block is the credibility artifact for LOE — the same role the "How we sized the annual benefit" table plays for the financial number. Without it, a "low effort" placement on a chart is just an assertion.

---

## The catalogue — axis pairs

Every entry: axes, units, scale, quadrant labels, win quadrant (varies — top-left or top-right depending on whether "less" or "more" is good on each axis), what counts as "good," and when to use. Axes follow natural orientation; the win quadrant is named per matrix.

### 1. Annual Benefit × Relative LOE

- **X-axis:** Relative LOE percentile (natural — lower = easier, left)
- **Y-axis:** Annual benefit ($M, recurring annual at full ramp)
- **Scale:** Linear both axes; log Y if portfolio top-to-bottom benefit ratio >20×
- **Quadrants:** Top-left = Quick wins / Top-right = Strategic bets / Bottom-left = Marginal effort / Bottom-right = Heavy lifts
- **Win quadrant: top-left** (high benefit, low LOE)
- **Bubble size:** Uniform on broad pool; sized by NPV after-tax on final portfolio
- **What good looks like:** Cluster in top-left
- **Use when:** COO / Operations audience, or any audience that needs the classic effort-impact framing. Default first matrix when audience is mixed or unspecified.

### 2. NPV × Payback (months)

- **X-axis:** Payback (months) (natural — shorter = better, left)
- **Y-axis:** NPV after-tax ($M, 5-yr cumulative; 7-yr if horizon trigger fires)
- **Scale:** Linear both axes
- **Quadrants:** Top-left = Fast & valuable / Top-right = Slow & valuable / Bottom-left = Fast & marginal / Bottom-right = Slow & marginal
- **Win quadrant: top-left** (high NPV, fast payback)
- **Bubble size:** Implementation cost (uniform on broad pool, sized on final portfolio)
- **What good looks like:** Top-left cluster, with a defensible long-tail in top-right for Phase 3 strategic bets
- **Use when:** CFO / Finance committee. Pairs with a strategic matrix when the audience is mixed CFO + CEO.
- **Skip when:** ≥2 candidates hit the payback cap (60 mo / 84 mo) — the cap clusters them at the right edge and obscures differentiation. Use NPV × Implementation Cost instead.

### 3. Cost Savings × Break-Even

- **X-axis:** Break-even (months from go-live to cumulative-positive) (natural — shorter = better, left)
- **Y-axis:** Cost savings ($M, recurring annual — Hard cost reduction + Productivity savings + Cost avoidance buckets only; not revenue)
- **Scale:** Linear both axes
- **Quadrants:** Top-left = Self-funding fast / Top-right = Self-funding slow / Bottom-left = Marginal & fast / Bottom-right = Marginal & slow
- **Win quadrant: top-left** (high cost savings, fast break-even)
- **Bubble size:** Uniform on broad pool, sized by cumulative cost savings on final portfolio
- **What good looks like:** Bundles that "pay for themselves" cluster in top-left
- **Use when:** CFO audience focused on cost discipline; finance committees evaluating self-funding portfolios; budget-pressured engagements where the case is "this funds itself"
- **Skip when:** Portfolio is >60% revenue-side benefit (Revenue assurance + Incremental revenue) — cost savings stops being the headline.

### 4. Benefit × Break-Even

- **X-axis:** Break-even (months) (natural — shorter = better, left)
- **Y-axis:** Annual benefit ($M, all five benefit classes — total economic value)
- **Scale:** Linear both axes
- **Quadrants:** Top-left = Fast & material / Top-right = Slow & material / Bottom-left = Fast & marginal / Bottom-right = Slow & marginal
- **Win quadrant: top-left** (material annual value, fast break-even)
- **Bubble size:** Uniform on broad pool, sized by NPV on final portfolio
- **What good looks like:** Top-left cluster
- **Use when:** Mixed-audience executive read-out where the audience wants the full benefit picture (not just cost savings) and a time-to-value frame. The most general-purpose financial matrix.

### 5. Strategic Anchor Strength × Annual Benefit

- **X-axis:** Strategic anchor strength (1–5 ordinal, derived from anchor count + anchor specificity per `anchor-specificity.md`) (natural — stronger = better, right)
- **Y-axis:** Annual benefit ($M)
- **Scale:** Linear both axes
- **Quadrants:** Top-left = Off-strategy & material / Top-right = On-strategy & material / Bottom-left = Off-strategy & marginal / Bottom-right = On-strategy & marginal
- **Win quadrant: top-right** (high anchor strength, high annual benefit)
- **Bubble size:** Uniform on broad pool, sized by NPV on final portfolio
- **Color overlay:** Map color by anchor cluster (per Phase 2 framework) instead of phase, when anchor-storytelling is the point of the matrix
- **What good looks like:** Tight top-right cluster proves the portfolio is anchor-aligned, not opportunistic
- **Use when:** CEO / Board / Strategy audience. Pairs with NPV × Payback when the audience is mixed strategy + finance.

### 6. EBITDA Impact × Time-to-Value

- **X-axis:** Time-to-value (months from go-live to ≥50% of full-ramp annual benefit) (natural — shorter = better, left)
- **Y-axis:** EBITDA impact ($M annual — benefit minus ongoing cost, no implementation amortization)
- **Scale:** Linear both axes
- **Quadrants:** Top-left = Fast EBITDA / Top-right = Slow EBITDA / Bottom-left = Fast marginal / Bottom-right = Slow marginal
- **Win quadrant: top-left** (high EBITDA impact, fast time-to-value)
- **Bubble size:** Uniform on broad pool, sized by NPV on final portfolio
- **What good looks like:** Tight top-left cluster shows the portfolio moves the EBITDA needle on a credible horizon
- **Use when:** Board, public-market-adjacent audiences (CFO + IR), or any engagement where the value frame is operating-margin expansion. Pairs well with Strategic Anchor × Benefit.
- **Note:** Avoid PE/exit framing language in titles and subtitles — see SKILL.md and global guidance. EBITDA impact is the metric, not the exit thesis.

### 7. P(NPV>0) × P50 NPV

- **X-axis:** Probability NPV > 0 (%) — from Monte Carlo (natural — higher = better, right)
- **Y-axis:** P50 NPV after-tax ($M) — from Monte Carlo
- **Scale:** Linear both axes (X bounded 0–100)
- **Quadrants:** Top-left = Low-confidence high-value / Top-right = High-confidence high-value / Bottom-left = Low-confidence low-value / Bottom-right = High-confidence low-value
- **Win quadrant: top-right** (high P50 NPV, high probability of clearing zero)
- **Bubble size:** Implementation cost
- **What good looks like:** Right side of the chart (P(NPV>0) ≥ 80%); top-right is the headline cluster
- **Use when:** Skeptical finance audience, audit committees, engagements where the disclaimer posture is HEAVY and confidence is the differentiator. Showcase that the recommendation isn't just point-estimate optimism.

### 9. IRR × Payback Period (investment-return view)

- **X-axis:** Payback period (months) (natural — shorter = better, left)
- **Y-axis:** IRR (%, unlevered project IRR over the modeled horizon)
- **Scale:** Linear both axes
- **Quadrants:** Top-left = Act now / Top-right = Strategic bet / Bottom-left = Fund it / Bottom-right = Reconsider
- **Win quadrant: top-left** (high IRR, fast payback)
- **Bubble size:** Implementation investment ($M one-time) — intentional: the size encodes how much capital is at stake, making the top-left quadrant visually compelling when low-investment UCs lead there
- **What good looks like:** Phase 1 quick wins cluster top-left; Phase 2 strategic bets appear top-right; deprioritized candidates fall bottom-right
- **Use when:** CFO / capital-allocation gatekeepers who think in hurdle-rate language. Most powerful when the client has a stated hurdle rate — add a horizontal dashed line at the hurdle rate and label it. Pairs naturally with NPV × Payback (#2).
- **Skip when:** The modeled horizon is <3 years for most candidates (IRR is unstable on short horizons); use NPV × Payback instead. Also skip when implementation cost variance across candidates is <2× — bubble sizing loses its signal.

### 8. Phase × Cumulative Investment (deployment view)

- **X-axis:** Deployment phase (Phase 1 / Phase 2 / Phase 3) — categorical
- **Y-axis:** Cumulative investment ($M, one-time)
- **Scale:** Linear Y; categorical X
- **Bubble size:** Annual benefit at full ramp
- **Color:** Phase (matches the existing AI Portfolio chart spec)
- **What good looks like:** Investment loaded in early phases pays back through Phase 2/3 benefit; visual confirms the staggered deployment thesis
- **Use when:** CIO / CTO audience focused on roadmap and capital allocation. Often shown in addition to a financial matrix.

---

## Audience → matrix shortlist

The skill recommends, the user decides. Caps: minimum 1, maximum 5. Default 1–2 unless the audience is heterogeneous.

| Audience | Recommended primary | Recommended secondary | Optional third |
|---|---|---|---|
| **CEO / Board / Strategy** | Strategic Anchor × Annual Benefit (#5) | EBITDA Impact × Time-to-Value (#6) | Annual Benefit × Relative LOE (#1) |
| **CFO / Finance committee** | NPV × Payback (#2) | Cost Savings × Break-Even (#3) | IRR × Payback (#9) or P(NPV>0) × P50 NPV (#7) |
| **COO / Operations** | Annual Benefit × Relative LOE (#1) | Benefit × Break-Even (#4) | Phase × Cumulative Investment (#8) |
| **CIO / CTO** | Annual Benefit × Relative LOE (#1) | Phase × Cumulative Investment (#8) | NPV × Payback (#2) |
| **CMO / CRO** | Benefit × Break-Even (#4) | Strategic Anchor × Annual Benefit (#5) | — |
| **Mixed exec / will be forwarded** | Annual Benefit × Relative LOE (#1) | NPV × Payback (#2) | Strategic Anchor × Annual Benefit (#5) |
| **Audit / risk committee** | P(NPV>0) × P50 NPV (#7) | NPV × Payback (#2) | — |

These are starting points. The skill should override the recommendation when:

- **MC results show the dimension doesn't discriminate** — drop matrices whose primary axis collapses to a narrow band
- **Portfolio is benefit-side heavy** (>60% revenue-class benefits) — drop Cost Savings × Break-Even even if CFO is the audience
- **Anchor count <3** — drop Strategic Anchor × Annual Benefit; the X-axis won't separate
- **Disclaimer posture = HEAVY and audience is finance-oriented** — promote P(NPV>0) × P50 NPV from optional to recommended

---

## Selection logic — what the skill does at Phase 6.5

1. **Read audience flag from intake** (Phase 1) and the Strategic Anchor Framework (Phase 2)
2. **Read MC outputs** from Phase 6 (per-candidate P10/P50/P90, P(NPV>0), composite rank)
3. **Compute discrimination check per candidate axis:** for each axis (annual benefit, NPV, payback, break-even, EBITDA impact, anchor strength, etc.), compute the inter-quartile range across the broad pool. If IQR < 20% of the median, the axis is flagged as low-discrimination — matrices using it as primary axis are demoted.
4. **Build shortlist:** 2–3 candidates from the audience table, filtered by discrimination check
5. **Present shortlist to user** with: recommended primary + secondary + optional, the rationale ("Audience = CFO; cost-savings axis discriminates well — IQR is 8× median"), and any demotions ("EBITDA impact dropped — IQR is 12% of median, won't separate visually")
6. **User decides** which to include (≥1, ≤5)
7. **Render** per the Rendering rules section below

---

## Rendering rules

### One canvas per matrix, separate sections

Each matrix renders in its own section on the AI Portfolio tab — not stacked on a shared canvas as small multiples. Each section carries:

- **Title** (sentence case, ≤8 words) — the storytelling claim. Examples: *"Where the easy wins live"* / *"Confidence vs. value, after Monte Carlo"* / *"Anchor alignment, sized."*
- **Subtitle (2–3 takeaways, ≤180 chars total)** — auto-drafted by the skill from the data on render, then user-editable in place. Examples:
  - *"8 of 12 bundles cluster <18-month payback. Phase 1 dominates the top-right. Two outliers in lower-left worth a closer read."*
  - *"Top-right = high anchor alignment + material value. Customer-trust anchor pulls the most weight (5 bundles, $42M)."*
- **Chart** at 480px height (see `design.md` — 10 for chart container specs)
- **Read-out paragraph (≤80 words)** below the chart, articulating the takeaway in plain language for the audience that will skim
- **Filters** — the existing Function / Strategic anchor / Phase filters apply to every matrix on the tab; a single filter row controls all charts simultaneously

Multiple matrices read top-to-bottom in the order recommended by the skill (financial first when the audience is finance-led, strategic first when the audience is strategy-led). User can reorder.

### Auto-drafted subtitle takeaways

The skill generates 2–3 takeaways per matrix from the rendered data. Templates:

- *"[N] of [N] bundles cluster [quadrant descriptor]."*
- *"[Phase / function / anchor] dominates the top-right."*
- *"[N] outliers in [quadrant] worth a closer read."*
- *"[Top-2 bundles by Y-axis] together represent [N]% of [Y-axis metric]."*

The user edits in place if a sharper claim is available. **Do not invent claims that the data doesn't support** — the auto-draft only states what's literally on the chart.

### Classification overlay (mandatory)

Every matrix carries a classification overlay so the audience can see at a glance which placements are point-estimate vs. assumption-driven. See `design.md` — 10 for the visual spec (dashed/solid borders, legend placement). This is non-negotiable — a "low effort, high impact" placement based on inferred LOE without the overlay is a credibility landmine.

### Bubble sizing

| View | Sizing |
|---|---|
| **Broad pool view (~50 candidates)** | **Uniform** — bubble size is a constant. Adding a third dimension to 50 bubbles overwhelms the chart. |
| **Final portfolio view (8–25 candidates)** | **Sized by a third metric** — typically NPV after-tax (default), implementation cost (CIO matrices), or annual benefit (where Y-axis is something else). The catalogue entry above states the default per matrix. |

The broad-pool view appears at Phase 6.5 for matrix selection; the final-portfolio view appears in the rendered HTML.

### Color encoding

Default: phase color (Phase 1 blue #0C62FB, Phase 2 teal #1BE1F2, Phase 3 purple #7B61FF).

Matrices show **only Slalom-proposed (net-new) bundles** as live data points (per `structural-rules.md` — AI Portfolio tab — Scope). In-flight initiatives stay on the Why Now tab.

Override default phase color when:

- **Strategic Anchor × Annual Benefit (#5)** uses anchor-cluster color instead of phase, since anchors are the storytelling primary
- **User overrides** for a specific narrative reason (document in Assumptions tab)

### Deprioritized candidates

Bundles deprioritized in Phase 7 appear on every matrix as greyed bubbles. See `design.md` — 10 for the visual treatment (50% opacity, neutral grey, dashed border). Hover reveals the bundle name + composite rank + reactivation note. Bubbles carry class `uc-bubble deprio-bubble` and **never get an onclick handler** — they're informational, not modal-bound.

**Dual-pool axis computation (Portfolio View Toggle).** When the Portfolio View Toggle is wired (per `portfolio-view-toggle.md`), the matrix SVG builder receives BOTH pools and computes Y-max and X-range from the **union** of the two — so deprioritized bubbles don't reflow the axes when the user switches between "Prioritized" and "All Evaluated" views. In Prioritized view, deprio bubbles are hidden via `body.view-prio .deprio-bubble { display: none }`; in All Evaluated view, they appear. The axes stay fixed across views.

This serves two purposes:

1. The audience sees the evaluation surface, not just survivors — reinforces that the final 8–25 was selected from a deeper pool
2. Anyone scanning the chart sees what nearly made the cut and where it lived on the dimensions that mattered

The greyed treatment is visually distinct from "considered but cut" candidates from Phase 3 — those don't appear on the matrix at all (they were never sized).

### Quadrant labels and the win-quadrant marker

Render the four quadrant labels in the chart background (faint grey, 11px, sentence case, positioned at the four corners). The labels per matrix come from the catalogue entry above.

**Mark the win quadrant explicitly.** The win quadrant varies by matrix — sometimes top-left (e.g., Annual Benefit × Relative LOE, NPV × Payback, where shorter/lower-effort sits left), sometimes top-right (e.g., Strategic Anchor × Annual Benefit, P(NPV>0) × P50 NPV). Render the win quadrant's label slightly emphasized — a small ★ glyph or a faint accent fill behind the label. The audience reads the chart faster when the win corner is named regardless of which corner it is.

---

## Matrix interactivity — click-to-filter

Every portfolio matrix must support click interaction. The matrix is not a static image — it's the entry point to per-UC detail. See `design.md` — 18 for the full implementation pattern (hit-position array, canvas click handler JS, cursor styling).

### Click behavior

| User action | Result |
|---|---|
| **Click a bubble/dot** | 1. Open the UC modal for that item. 2. Filter the portfolio table below to show only that UC's row. 3. Show a "Show all use cases" reset button above the table. |
| **Click empty chart space** | Reset the table filter to the current function filter (or "all" if no function is selected). |
| **Press Escape** | Close the modal. Table filter remains (user may want to see the filtered row after closing). |
| **Click the reset button** | Reset the table filter. |

### Visual cues

- Set `canvas.style.cursor = 'pointer'` after drawing bubbles
- The chart legend should include: *"Click a bubble for details."*
- Label each bubble with its UC ID (or abbreviated ID) when the bubble radius is large enough (> 10px)

### Redraw clears hits

When the chart redraws (on function filter change), clear the `bubbleHits` array first. Stale hit positions from a previous draw will produce incorrect click targets.
