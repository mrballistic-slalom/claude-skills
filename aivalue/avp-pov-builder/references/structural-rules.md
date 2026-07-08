# Structural Rules

What's fixed across every PoV vs. what's rebuilt per client/topic. This is the contract: don't innovate on the fixed parts; do tailor the flexible ones.

**Visual implementation specs (CSS, component templates, chart containers, interaction JS, tooltips, nav bar styling) have moved to `design.md`.** This file now focuses on information architecture — what content goes where, in what order, and under what constraints.

> **Build process rules live in SKILL.md — Phase 9 build contract** — the DO / DO NOT numbered rules and the deviation gate (always ask the user before deviating from the skeleton structure). This file describes *what* goes in each tab; the build contract governs *how* the HTML is produced.

---

## Fixed structure (every PoV)

### Tab structure — canonical 7-tab default with 5-tab variant

**Default 7-tab structure** (the canonical layout — Summary is hero-only, depth lives on dedicated tabs; Assumptions and Sources are split into separate tabs to keep each focused):

1. **Summary** — single-screen executive summary. Disclaimer band + hero only: title + tagline + the big-one metric + 2×3 supporting KPI strip + Phase 0/1/2/3 strip + 1-line context bridge. **Nothing else.** No bridge waterfall, no Why Now, no anchors, no AI Success Patterns — those live on the Why Now tab.
2. **Why Now** — disclaimer + In-flight acknowledgment section *(when applicable per net-new vs. in-flight rule — see — In-flight section below)* + portfolio bridge + Why Now (forcing functions) + Strategic alignment ("Your goals. Our analysis.") + AI Success Patterns. The narrative defense of the Summary.
3. **AI Portfolio** — disclaimer + **one or more matrices selected at Phase 6.5** (≥1 hard rule, max 5 — see `portfolio-matrices.md`) + filterable table + evaluated-but-deprioritized panel (mandatory when deprioritized count > 0) + considered-but-cut panel (mandatory when cut count > 0).
4. **AVP Analysis** — *(optional, only if the user provided one or more value-chain images — see Question 10 of `intake-checklist.md`).* Disclaimer + N value-chain images (one per assessed business function) per multi-image spec, OR single image, OR omit if no images provided. Section eyebrow uses **"AVP TASK ANALYSIS"** — visible AVP positioning on this tab is intentional.
5. **Roadmap** — disclaimer + **(fixed)** cumulative cost-vs-benefit SVG line chart with break-even crossover annotation + Phase 0 callout (foundation investment excluded from portfolio totals) + **(5-view toggle)**: **Overview** (Phase 1/2/3+ deployment cards with UC list, one-time/ongoing/annual-benefit per phase, cost breakdown table) · **Workstreams** (SVG swim lane across 48-month horizon: Foundation track, per-UC build/operate bars, Change Management as persistent track, Value Realization track; phase background bands; month x-axis) · **Phase Gates** (one go/no-go card per phase boundary: timing badge, 4 explicit pass criteria derived from engagement KPI targets, "on no-go" consequence block) · **Dependencies** (one card per portfolio UC: Data / Platform / Org readiness / Predecessor blocks, with Predecessor either "None" or citing the specific prerequisite UC/platform state) · **Horizons** (three cards mapping Phase 1→Horizon 1 Productivity Assist+Automate, Phase 2→Horizon 2 Differentiation Augment+Anticipate, Phase 3+→Horizon 3 Disruption Associate+Agentize; each card carries colored 6As pills, UC assignments, and key measurement signals).
6. **Assumptions** — disclaimer + Monte Carlo confidence (P10/P50/P90 + probability strip + plain-language summary) + Company/sector profile + Inferred assumptions table `[I#]` + Gaps & limitations + Model methodology (horizon, realization factor, MC methodology). **Skeleton pattern (pre-citation-system):** four interactive DCF parameter sliders (WACC · FTE cost · Year 1 adoption rate · implementation cost buffer) with live propagation to Portfolio tab figures and totals + three static assumption cards (Financial Model · Technical · Delivery). Replace with `[I#]` table + MC confidence bands once citation routing is active.
7. **Sources** — disclaimer + Primary source signals table `[S#]` + Benchmark library table `[B#]` + Research methodology paragraph. **Skeleton pattern (pre-citation-system):** filterable citation cards grouped by type (Market Research · AI Benchmarks · Slalom IP · Client Data), each tagged with the UCs it supports. Replace with numbered `[S#]`/`[B#]` tables + "Used for" column once citation routing is active.

**Tighter 5-tab variant** (when editorial restraint matters most):

1. **Summary** — same as 7-tab default
2. **AI Portfolio** — folds Why Now content in as a top section
3. **Roadmap**
4. **Assumptions**
5. **Sources**

(AVP Analysis is optional regardless of variant — depends on whether the user provides images.)

**Deciding between variants:**
- 7-tab when the audience expects depth across multiple tabs (default)
- 5-tab when the audience is an executive group and editorial restraint is the priority
- Default to 7-tab if uncertain — easier to compress later than to expand
- AVP Analysis tab is included in the canonical 7-tab default (or 5-tab variant) only when the user provides one or more value-chain images at intake; if no images, the AVP Analysis tab is omitted entirely (count drops to 5-tab / 4-tab respectively)

### Tab IDs — naming convention

Tab IDs in HTML (`<div id="tab-...">` and `showTab('...')` calls) are case-folded, hyphen-free slugs of the tab name:

| Tab name | Tab ID |
|---|---|
| Summary | `tab-summary` |
| Why Now | `tab-whynow` |
| AI Portfolio | `tab-aiportfolio` |
| AVP Analysis | `tab-avpanalysis` |
| Roadmap | `tab-roadmap` |
| Assumptions | `tab-assumptions` |
| Sources | `tab-sources` |

This convention is enforced — alternate IDs (`tab-overview`, `tab-phasing`, `tab-portfolio`, `tab-avp`, etc.) are legacy and should be migrated. The QA panel-placement check (per `qa-checklist.md` — Panel placement) iterates over this exact list.

### Citation routing

Body-text citation references route to the correct tab on click:

| Prefix | Body usage | Click behavior |
|---|---|---|
| `[S#]` | Primary source — 10-K, 10-Q, earnings transcript, press release, regulatory filing, named partner case study | Switch to **Sources tab** + scroll to row |
| `[B#]` | Benchmark — consulting research, analyst report, industry association data | Switch to **Sources tab** + scroll to row |
| `[I#]` | Inferred — Slalom modeled assumption, derivation chain, comp-derived parameter | Switch to **Assumptions tab** + scroll to row |

Each row in the destination tab carries `id="ref-S1"` / `id="ref-B3"` / `id="ref-I5"` for direct linking. See `design.md` — 16 for the CSS animation highlight on arrival.

---

### Summary — section order (top to bottom)

**The Summary tab is a single-screen executive summary. Hero only. Nothing else.**

1. **Disclaimer band** — see `design.md` — 7 for visual spec
2. **Hero** — title + tagline + the big-one metric + 2×3 supporting KPI strip + Phase 0/1/2/3 strip + Phase 0 caveat. **No diagonal watermark.** See `design.md` — 8 for full visual spec.
3. **Single-line context bridge** — one sentence below the hero connecting to the rest of the dashboard (e.g., *"The story behind these numbers continues on the next tab."*)

**That is the entire Summary tab.** Bridge waterfall, Why Now, Strategic alignment, AI Success Patterns, full phase deep-dive — all live on **Why Now** (Tab 2 in the 7-tab default) or are folded into AI Portfolio (in the 5-tab variant). This is the "tell the story with less, not more content" principle.

### Why Now — section order (Tab 2 in 7-tab default)

1. **Disclaimer band**
2. **In-flight acknowledgment section** *(when applicable — see — In-flight section below)*. Renders at the top of the tab before "What Slalom adds" when inputs exist.
3. **Portfolio bridge visual** — narrative sentence + scope waterfall + function cards + phase investment/value cards. See `design.md` — 9 for visual spec.
4. **Why Now (forcing functions)** — 3–4 forcing functions (industry shift, regulatory change, competitive AI threat, internal program window). Each grounded in primary sources with citations.
5. **Strategic alignment** — "Your goals. Our analysis." Cards mapping use cases to stated strategic objectives (Pattern A or B from — Strategic Alignment).
6. **AI Success Patterns** — four patterns, topic-mapped (heading: "AI SUCCESS PATTERNS")
7. **The execution path** — Phase cards (Phase 0/1/2/3) with KPIs and clickable UC tiles. *(In 5-tab variant this content moves to the Roadmap tab.)*
8. **Exit value thesis** *(optional)* — frame AI outcomes as precursors to the metrics that determine business value. Include when the client's competitive position or valuation is the strategic frame. Always carry "— illustrative" on the sec-eye.

---

### In-flight section (Why Now tab, top, when applicable)

When the engagement has acceleration plays from primary-source research, OR a client AI backlog from intake, OR both, render a "What [client] has in flight" section at the top of the Why Now tab (before "What Slalom adds").

**Section structure:**

- **Section heading:** *"What [client] has in flight"* or equivalent (avoid "named publicly" — see `editorial-rules.md` — Banned vocabulary)
- **Lede paragraph (2–3 sentences):** inputs sourced (research / backlog / both), aggregate count, aggregate sized value, citation provenance
- **Card grid** (4-col responsive): one card per in-flight initiative, with:
  - Status pill: *in production / in deployment / active collaboration / in build / announced for launch*
  - Initiative name
  - Named partners (if any)
  - Scope (1-line)
  - Anchor mapping
  - Sized annual value
  - Citation chip(s)
- **Sub-total card** at end of grid showing aggregate sized value
- Cards are **NOT** clickable to modals — they're acknowledgments, not proposals

**Visual treatment:** See `design.md` — 14 for card styling, status legend template, and Mode C visual distinctions.

**Omission rule:** If neither inputs source yields anything, omit this section entirely. Note in the Sources tab methodology paragraph: *"Client AI work in flight: not surfaced in this PoV; to be discovered during validation."*

---

### The Disclaimer band

Content requirements — see `design.md` — 7 for visual spec:

- **Appears at the top of every tab panel** — not just the Executive Summary
- Language calibrated to classification mix (see `classification-rules.md`)
- Always includes: "illustrative analysis only", "do not represent actual cost commitments", "validation through discovery required"
- "Note on scope:" — states what's included (organizational enablement, compute/infrastructure) and what's excluded (Phase 0 foundation). Inline, no carriage return after the colon.
- "Currency note:" — states the currency convention. Inline, no carriage return after the colon.
- Full disclaimer is the standard: 3 paragraphs covering illustrative basis, methodology transparency, and validation requirement

---

### The Hero pattern

The hero is the entire content of the Summary tab. Three elements work together: **title + tagline + the big-one metric**. Below those sits the supporting 2×3 KPI strip and the Phase 0/1/2/3 strip.

**Title + tagline + the big-one form a coherent narrative triangle.** Compelling but truthful. The skill enforces no overclaim and no contradiction across the three. See `editorial-rules.md` — Narrative cohesion.

**Each hero element must ground in a publicly stated client priority or commitment.** The hero is not creative copy — it is a translation of the company's own published strategic objectives into a transformation framing. If a candidate cannot tie back to a stated priority, a 10-K disclosure, an earnings-call commitment, an investor-day target, or a CFO-defensible financial proof, it is the wrong candidate.

#### Options-driven build process

**Title, tagline, and hero metrics are not auto-generated — the skill presents options.**

For each, the skill:
1. Generates 3–5 candidates grounded in the client's brand language, stated priorities, financial reality, and competitive context
2. Ranks by fit-to-audience and compelling-story potential
3. Recommends one with rationale
4. Lets the user pick, request alternatives, or write their own

This pattern repeats for **title** (3–5 options), **tagline** (2–3 options once title is chosen), and **hero metrics** (the big-one + supporting six). See `intake-checklist.md` — Hero options.

**The big-one — the single dominant takeaway**

A 7th metric, sized larger than the supporting strip, positioned above it in the hero. The big-one is the number the audience should remember if they remember nothing else — picked specifically for the audience and the compelling story.

The skill recommends the big-one based on:
- **Audience** — CEO/Board sees scale narrative; CFO sees after-tax NPV; CIO sees deployment-ready scope; CMO sees revenue lift
- **Story strength** — what's the most defensible, freshest, biggest number?
- **Truthfulness** — never over-rounded, never combined misleadingly across timing, never overclaimed

#### Hero element examples — tied to strategic objectives

Examples below use bracketed placeholders (`[N]`, `[$N]`) so they don't accidentally mirror a real client number. Each shows how the hero element grounds in a publicly stated objective, regardless of industry.

| Hero element | Example                                          | Ties to                                                          |
|---|---|---|
| Title    | *"Three platforms. One AI strategy."*                | Replatforming program named in 10-K and earnings calls           |
| Title    | *"[N] million customers. One AI engine."*            | Customer-base scale disclosed in annual report                   |
| Title    | *"From [N] [pilots/initiatives] to a portfolio."*    | Acceleration plays disclosed publicly; positions the PoV as scaler |
| Title    | *"The next decade of [domain] starts here."*         | Aspirational, future-facing — anchors to a stated horizon goal   |
| Tagline  | *"An AI roadmap for [stated priority area]."*        | Maps directly to a stated FY priority                            |
| Tagline  | *"[Domain] transformation at the scale of [stated commitment]."* | Anchors scope to a published target              |
| Big-one  | *"[$N]M after-tax NPV"*                              | CFO-defensible financial proof                                   |
| Big-one  | *"[N]M-customer precision at 1:1 scale"*             | Scale × personalisation narrative for CEO/board                  |
| Big-one  | *"+[$N]M incremental annual revenue"*                | Top-line story for CMO/CRO                                       |
| Big-one  | *"[N] use cases · [N] strategic anchors"*            | Deliverability frame for CIO                                     |

#### Subtitle line

A single connecting sentence that spans the hero box, bridging title to dashboard content. Often the tagline itself, when the tagline is long enough; otherwise a separate line. No data, no scope counts — just context.

#### Visual spec

See `design.md` — 8 for the full hero visual spec (gradient, type sizes, KPI strip layout, phase strip, Phase 0 caveat).

---

### The Portfolio Bridge Visual

Two-layer visual inserted between the hero and strategic alignment. See `design.md` — 9 for visual spec (node sizes, centering, function card treatment, phase card colors).

**Layer 1 — Narrative sentence:**
A single sentence above the bridge that tells the story: *"We mapped [client]'s operational value chain across [N] operations, identified [N] key activities, surfaced [N] potential AI enhancements — and assembled [N] prioritised use cases aligned to your stated strategic objectives, grounded in the operational challenges of scaling to [target]."*

Client-facing terminology throughout (see SKILL.md — Client-facing terminology).

**Layer 2 — Scope waterfall** (horizontal chain, centred):
- Nodes: [N] Operations assessed → [N] Key activities mapped → [N] AI enhancements identified → [N] Prioritised use cases → [value metric]

**Layer 3 — Function cards** (one per assessed operation):
- Function name, use case count, feature count, task count
- NPV or primary value contribution
- Value driver label if applicable

**Layer 4 — Phase investment/value cards:**
- Phase 0 (always TBC) + Phase 1 + Phase 2
- Each: investment, primary value metric, avg payback, constituent use case list

---

### Strategic Alignment — "Your goals. Our analysis."

**Mandatory section.** Appears between the bridge and AI Success Patterns on the Why Now tab (or as the second section after Why-now content in the 5-tab variant where it is folded into AI Portfolio).

**Introductory text:** A 2-3 sentence paragraph stating that every use case maps to a goal the client has communicated (to investors, in public statements, or directly to the team). Source citations inline.

**Anchor specificity is required** — see `anchor-specificity.md`. Generic phrasing that could apply to any client in the same industry fails the bar.

**Two layout patterns:**

#### Pattern A — Equal-card grid (default for ≤4 anchors)

One card per strategic anchor, presented in a uniform grid. Each card contains:
- Anchor name (e.g., "Geographic expansion")
- Source citation(s) as clickable references
- Subtitle with the specific target (e.g., "180–200+ U.S. boutiques")
- Use case count mapped to this anchor
- Aggregate value (NPV or annual value) of mapped use cases
- 2-3 sentence description of why this anchor matters and how AI addresses it
- Mapped use case IDs listed at the bottom

#### Pattern B — Thematic clustering (preferred for 5+ anchors)

When the anchor count exceeds ~4, six equal cards in a 3×2 grid produce a "row of boxes" feel that reads as catalog rather than synthesis. **Cluster anchors into 3 strategic themes** with the UC linkage made explicit at the theme level. See `design.md` — 23 for the layout pattern.

Theme names should be 2-3 words and articulate the strategic posture (e.g., "Growth & Transition" / "Reliability & Customer" / "Operating Model"). Each theme header carries the union of UC IDs driven by its constituent anchors.

Each anchor mini-card under a theme is a simplified version: heading + citation, target line, stats (UCs · Annual value), and a single-line takeaway (cut the long "why this matters" paragraph since the takeaway compresses it).

**For publicly traded companies:** Anchors are sourced from filings, earnings calls, investor day presentations. Every anchor must have at least one source citation.

**For privately held companies:** Anchors may come from web research, comp analysis, and user-provided context. Citation quality will vary — note the basis in each card.

---

### AI Success Patterns

- Section eyebrow: **"AI SUCCESS PATTERNS"** (not "Slalom's Assessment Framework")
- Always all four patterns — don't drop, don't add
- Each card: number (01–04) + pattern name + tagline + generic statement + topic-specific callout
- Lead paragraph cites Slalom 2024 Executive Perspectives + leading consulting research (both)
- Proof strip below cards maps the portfolio to all four patterns

---

### The Execution Path (Phase cards) — default is four phases

**Default phasing is Phase 0 / 1 / 2 / 3.** Four phase deployment cards in the Roadmap tab Overview view, not three. The previous default of three phases (Phase 0 + Phase 1 + Phase 2) collapsed too many use cases into Phase 2 and lost the Phase 3 "function reshape" narrative.

Phase labels (use plain language; avoid arrow-and-verb-noun jargon — see `editorial-rules.md` — Banned vocabulary):
- **Phase 0 — Foundation work.** Always present, always TBC dollar figures, always parallel-track to Phase 1.
- **Phase 1 — Deploy Year 0.** 5-year ramp.
- **Phase 2 — Deploy Year 1.** 4-year ramp.
- **Phase 3 — Deploy Year 2.** 3-year ramp. Reserved for the deepest workflow redesigns and capabilities that depend on Phase 1 + 2 being live.

Topic-specific plain-language alternatives are also acceptable when they describe what the phase actually does for that engagement.

Each phase card: badge with phase name, subtitle, investment (one-time) + annual benefit at full ramp (recurring annual) + avg payback (months), clickable UC tile list. See `design.md` — 17 for the Phase 0 card template.

**Phase 0** is foundation work (governance, cloud platform standardization, MLOps tooling, responsible AI framework, regulatory assurance overlays specific to the client). Always TBC, always scoped during validation. Phase 0 use cases are not in the financial portfolio.

**Omit Engagement Intensity by Phase grid by default.** Include only if the user explicitly requests it.

---

### AI Portfolio tab — Portfolio & Prioritisation (Tab 3 in 7-tab default)

**Scope:** The matrices and filterable table show **only Slalom-proposed (net-new) use cases**. The in-flight set is acknowledged separately on the Why Now tab — it does not appear in any matrix or the filterable table.

**Optional in-flight strip (above the first matrix):** See `design.md` — 14 for visual spec.

**Matrix block — at least one matrix, up to five.** The AI Portfolio tab carries 1–5 matrices selected at **Phase 6.5 — Matrix selection** per `portfolio-matrices.md`. The **≥1 matrix rule is a hard rule** — every PoV ships at least one matrix on this tab. See `design.md` — 10 for chart container specs and rendering rules.

Each matrix renders in its own section with title, subtitle, chart, and read-out paragraph. See `portfolio-matrices.md` — Rendering rules for the full spec.

**Classification overlay (mandatory on every matrix):** see `design.md` — 10. Without the overlay, a "fast payback, high benefit" placement based on inferred inputs is a credibility landmine.

**Deprioritized candidates render greyed on every matrix** — see `design.md` — 10.

**Filters:** A single filter row controls all matrices simultaneously — Function, Strategic anchor, Phase.

**Table:** All Slalom-proposed use cases, sortable by all columns. Default sort: primary value metric descending. Columns: ID, Name, Function, Phase, LOE, Annual value, NPV, Payback, Strategic anchors (as pills).

**Detail expand:** Click any row → inline expansion showing: description, feature count, benefit type, annual benefit, implementation cost, ongoing cost breakdown, strategic anchor tags, and citation references. Every detail row includes classification statement: *"INFERRED — benefit estimates require validation against [client]'s actual operating data."*

**"Considered but cut" panel — MANDATORY when cut count > 0**

Below the active portfolio table, render a panel with:
- **Heading:** *"What we considered but didn't propose"* (or equivalent — avoid jargon)
- **Lede (~50 words):** explains the panel exists for transparency — bundling rigor visible to the reader
- **Table:** ID · candidate use case · function · why cut
- See `design.md` — 22 for visual treatment

**"Evaluated but deprioritized" panel — MANDATORY when deprioritized count > 0**

Below the "Considered but cut" panel. These candidates have a different evidentiary status — fully sized and MC-tested.
- **Heading:** *"Evaluated, sized, and tested — deprioritized for this portfolio"* (or equivalent)
- **Lede (~60 words):** explains that these candidates were part of the ~50-candidate broad pool, received full financial treatment and Monte Carlo analysis, and were deprioritized based on composite ranking.
- **Table:** ID · use case · function · composite rank · P50 NPV · P(NPV>0) · reason deprioritized · reactivation note
- See `design.md` — 22 for visual treatment (distinct shade from "considered but cut")
- **Panel emphasis is view-aware** when the Portfolio View Toggle is wired (see `portfolio-view-toggle.md`). Apply class `deprio-panel` to the wrapper; `body.view-prio` styles it at `opacity: 0.85` (muted), `body.view-all` styles it with `border: 2px solid var(--slalom-blue)` and a tinted header (emphasized). The "All Evaluated" framing must never claim the dashboard recommends the deprioritized items — keep the *"evaluated and deprioritized — not ignored"* framing with reactivation triggers per UC.

---

### Legacy/optional — Readiness & Vulnerability tab

**Not in the canonical 7-tab default.** This was a tab pattern from earlier dashboard variants, retained here as a documented option for engagements where a scored readiness + vulnerability assessment is genuinely warranted. Add it as an extra tab only if the user explicitly requests it at intake.

If used, two-part scored assessment. Both parts carry **"— ILLUSTRATIVE"** on their sec-eyes.

**Part A — Readiness Scorecard** (7 dimensions, scored 0–5):
- 1 Strategy & Use-Case Maturity
- 2 Data Foundation
- 3 Technology & Infrastructure
- 4 Talent & Operating Model
- 5 Security, Privacy & Cybersecurity *(full-width card; three sub-panels: Access Control strength / AI & LLM Threat Surface gap / Cross-Client or High-Risk Data risk; explicit on prompt injection, hallucination in safety-critical paths, vendor concentration)*
- 6 Financial Capacity
- 7 Change Readiness
- Each dimension: score badge, evidence body, basis note with source citations

**Part B — Vulnerability Assessment** (5 areas):
- A Business Model / Growth Sustainability
- B Competitive Dynamics
- C Customer & Market Sensitivity
- D Talent & Capability Risk
- E Operational Risk — AI Cybersecurity, Model Risk & Vendor Exposure

**Part C — 90-Day Execution Plan** (bottom of the legacy Readiness tab):
- 4-column grid: weeks 1–2 / weeks 3–4 / weeks 5–8 / weeks 9–12
- Each column: label, title, bullet activity list
- Acceptance criteria block: numbered ①–⑥, explicit and measurable
- Scope commitment: **2–3 proof-of-value use cases in 90 days**

---

### Legacy/optional — Strategic Context tab

**Not in the canonical 7-tab default.** Strategic context content is folded into the Why Now tab (forcing functions + Strategic alignment sections). Retained as a documented option for engagements where a dedicated context tab is requested. If used, the three sections below apply.

Three sections:
1. **Client's stated strategic goals** — the strategic anchors from the framework, presented as goal cards with source citations, mapped use case IDs, and "why this matters" context.
2. **Forcing functions** — tariff environment, regulatory changes, competitive dynamics, macroeconomic pressures that create urgency. Ground in current events with source citations.
3. **Competitive dynamics** — industry-level competitive framing. Do NOT name specific competitors unless they are publicly discussed by the client in their own filings.

---

### Per-UC modal — required architecture (10-section spec)

Every UC in the data model is clickable from any matrix on the AI Portfolio tab, the filterable table, and the phase cards. Clicking opens a modal with the following 10-section spec, in order.

1. **Header pills** — strategic-fit tier (HIGHEST/HIGH/MEDIUM-HIGH/MEDIUM) · phase (1/2/3) · LOE tier (Quick Win / Standard / Major Initiative — categorical, distinct from the relative LOE percentile in Section 7B) · ID
2. **Title + benefit-class subtitle** — UC name + 1-line benefit-class description (e.g., "Productivity savings · Care productivity + recognition fulfillment")
3. **KPI strip (4 cards)** — Annual benefit (recurring annual) · 5-yr after-tax NPV (cumulative) · Implementation (one-time, incl. enablement) · Payback (months). Every metric labeled with timing modifier.
4. **What it is** — 3–5 sentence narrative description
5. **Who uses it at [client]** — bullet list of 3–5 primary roles affected (real client job titles, not generic categories)
6. **Benefits beyond the dollar value** — 4–6 specific bullet benefits per UC (operational, customer, risk, etc.)
7. **Sizing transparency — benefit and effort.** Two paired credibility blocks. **Together the strongest credibility artefacts in the modal** — every row carries a citation chip ([S#]/[B#]/[I#]).
   - **7A. How we sized the annual benefit** — Step → Value → Source table with the final calculation row highlighted. See `design.md` — 24 for the visual template.
   - **7B. How we scored the relative LOE** — required block per `portfolio-matrices.md` — Rationale + assumptions in the deep-dive tile. Contains: headline (*"Relative LOE: [N] / 100 ([percentile descriptor])"*), component breakdown table, reasoning paragraph (≤120 words), key assumptions bullet list (≤5 items, tagged `[I#]` when material).
8. **Monte Carlo confidence ranges** — see `design.md` — 25 for the range bar and probability badge visual spec.
9. **Strategic anchors + technology & data** — anchor pills for each anchor this UC supports, then tech stack pills (named partners only — see `primary-source-research.md` — Public-language hygiene). See `design.md` — 13 for tech-pill solid/dashed treatment.
10. **AVP source attribution** — feature count + average AVP strategic-fit score (for QA traceability) + brief note on which AVP-derived operation(s) contributed.

**Closing disclaimer** — italic ILLUSTRATIVE block reaffirming HEAVY disclaimer language; specifically calls out that Monte Carlo bands are sensitivity, not added precision.

**Modal sizing:** see `design.md` — 12. Modals are for Slalom-proposed (net-new) UCs only.

---

### Capability-graph ingestion (subway-map pattern)

When the source POV deck includes a navigation-style diagram of capabilities (e.g., a "5 pillar offerings × N capabilities" map across a horizontal flow), translate to an interactive subway-map visualisation rather than a static image.

**Spec:**
- One horizontal track per pillar, color-coded
- Capability "stations" (circles) along each track
- Each track ends in a "destination" badge carrying the outcome statement
- Hover tooltips on every station, every track label, and every destination, each with two parts:
  1. **What it is** — the general definition
  2. **How it applies to [client]** — concrete connection
- Legend strip in the section header

This pattern applies whenever the source deck has a navigation-style diagram of capabilities — typically a multi-pillar offerings grid feeding into outcome destinations.

**Anti-pattern:** rendering the capability graph in three different views on the same tab. Pick *one* canonical view; tooltips on the canonical view should carry the supporting context that the other views would have shown.

---

### AVP Analysis tab (optional)

**Built only when the user provides one or more value-chain images at intake (Question 10 of `intake-checklist.md`).** If no image, omit the tab entirely — don't ship a placeholder.

**Tab name and ID:** The tab is labeled **"AVP Analysis"** in the nav (visible AVP positioning is intentional on this tab). The tab ID is `tab-avpanalysis`. The section eyebrow inside the tab is **"AVP TASK ANALYSIS · AI readiness across the value chain"**.

**Two modes — single-image or multi-image:**

**Single-image mode:**
- 1 paragraph framing → 1 image card → 1 reading-the-coloring legend → 1 paragraph implication

**Multi-image mode (preferred when AVP covers ≥2 functions):**
- 1 paragraph framing (~80 words) covering all functions
- N function sections in function-number order, each with:
  - Sub-heading: function ID + name
  - 1-line context (function descriptor + AVP feature count if known)
  - Image card (full container width, base64-embedded inline)
- 1 reading-the-coloring legend (after all images, once)
- 1 paragraph implication (~80 words) covering all functions

**The reading-the-coloring legend:** small inline legend translating the color coding (typical: green = high readiness, yellow = medium-high, orange = medium-low, red = low). Rendered once, after all images.

**What the framing paragraph covers:**
- What the visualization(s) show: the operational value chain mapped from L1 (operational areas) → L2 (processes) → L3 (key activities), color-coded by AI readiness
- That this is the analytical input that drove the use case prioritization seen on the AI Portfolio tab

**Anti-patterns:**
- Shipping an AVP Analysis tab with no image (placeholder text is worse than omission)
- L3 tasks as colored chips with role + AI-readiness % visible (too dense for this tab — the image itself is the visual; text-based reconstructions are secondary)

---

## Standardized vocabularies (do not invent alternatives)

### Strategic-fit tier — four values

Every use case carries one of these four tiers. The vocabulary is fixed across all PoVs.

| Tier | When to use |
|---|---|
| **HIGHEST** | Direct map to the company's most-named priority (a CEO quote, a stated FY priority). The headlines for the dashboard. |
| **HIGH** | Strong alignment with stated priorities — a named anchor with a published target, or a regulatory/compliance constraint with a public anchor. The strong secondary set. |
| **MEDIUM-HIGH** | Aligned with stated priorities but indirect path — supports a stated priority but not a top-named focus area. |
| **MEDIUM** | Operationally valuable but not directly tied to a stated priority. Frame as "supporting" or "foundational." |

Don't invent alternative tier names — consistency across PoVs is part of the credibility signal. See `bundling-logic.md` — Step 4 for assignment logic.

### Citation ID system — fixed prefixes

Every quantitative claim in body tabs gets a superscript clickable reference. Three prefixes, fixed:

| Prefix | Meaning | Example | Routes to |
|---|---|---|---|
| `[S#]` | Primary source | `[S1]`, `[S12]` | Sources tab |
| `[B#]` | Benchmark | `[B1]`, `[B4]` | Sources tab |
| `[I#]` | Inferred | `[I1]`, `[I5]` | Assumptions tab |

Numbering is sequential within each prefix, in order of first appearance. Click behavior: switches to the destination tab AND scrolls to the specific row. See `design.md` — 16 for the highlight animation.

---

## Flexible (rebuild per client/topic)

- Hero headline and subtitle (aspirational framing rebuilt per client)
- Topic title and subtitle
- Why Now tab framing (the forcing-function narrative is client-specific)
- Strategic alignment anchors and context paragraphs (rebuilt from the Phase 2 strategic anchor framework)
- The use cases and their names, descriptions, financial estimates
- Archetype or value bucket names (rebuild per topic)
- Phase descriptions (labels fixed; copy changes)
- AI Success Patterns "In [topic]:" callouts
- Industry benchmarks cited
- Whether to include the exit value thesis section
- Depth of any optional Readiness/Vulnerability tab if requested
- Financial metric selection for hero, KPIs, and chart (see `financial-model.md`)
- Matrix selection on the AI Portfolio tab — which axis pairs render and in what order (see `portfolio-matrices.md`)

---

## Nav bar

See `design.md` — 6 for the complete CSS spec, logo handling rules, and nav title formatting.

---

## Standard components

Standard component HTML/CSS templates have moved to `design.md` — 17. Engagement-specific values are consumed from `engagement-config.md`. The templates cover:

- **Glossary panel** (Summary tab) — `<details open>` panel with financial and AVP terms
- **Methodology visual** (Sources tab) — seven horizontal phase cards
- **"Used for" column** on Primary sources table (Sources tab) — four columns: ID / Source / Type / Used for
- **Gap-explanation paragraph** (Assumptions tab) — blue-bordered callout reconciling benchmark percentages against modeled dollars
- **Tech-pill solid/dashed treatment** (UC modals) — solid = existing stack, dashed = net-new
- **In-flight status legend** (Why Now tab) — status definitions for in-flight cards
- **Anchor tooltips** — CSS tooltips on every anchor code reference
- **Phase 0 cards** (Roadmap tab) — never show TBC; render with engagement-specific dollar anchor
- **Break-even callout** (Roadmap tab) — live, function-aware callout synced with filter
- **Filter-sidebar prompt** — one-line subtext explaining the filter behaviour
- **Portfolio View Toggle** (top of function-filter sidebar) — **REQUIRED when any candidate was deprioritized (downselect ratio < 1.0)**. Two stacked buttons (Prioritized ↔ All Evaluated) swap the visible pool. Suppressed only when downselect ratio = 1.0 (broad pool == final portfolio). When suppressed, add `<!-- portfolio-toggle-suppressed: ratio=1.0 -->` inside the sidebar div. Composes with the function filter via `body.view-*` + `body.filter-*` classes. The `setView` JS function must be defined when the toggle is rendered. See `portfolio-view-toggle.md` for the complete spec. **Missing toggle when ratio < 1.0 = hard fail in `qa-automated-checks.py`.**
- **Forcing-card structure** (Why Now tab) — title + tagline + body
- **Skill attribution footer** (every tab) — **HARD FAIL if absent on any tab.** `<div class="skill-attribution">Generated using Slalom ACS[YYYYMMDD]</div>` at the bottom of every tab panel — inside the tab-panel div, after all other content, before the closing `</div>`. `[YYYYMMDD]` = the `updated` date from SKILL.md frontmatter, no separators (e.g. `2026-05-27` → `ACS20260527`). CSS: `font-size:11px; color:var(--muted); text-align:right; padding:12px 0 4px; border-top:1px solid var(--line); margin-top:32px`. Count must equal tab count — `qa-automated-checks.py` S5 enforces this. The `build-skeleton.html` golden master includes this footer on all 7 canonical tabs as of v2.5.

### "Used for" column on Primary sources table (Sources tab)

The Primary sources table carries four columns: ID / Source / Type / **Used for**. The Used-for value maps each citation to where it's referenced in the dashboard. The Used-for content is auto-populated from `engagement-config.md` — 10 (the source mapping derived by walking citation references in the rendered HTML). Manual edits are allowed for clarity.

### Mandatory per-UC "How we sized this" section

Every UC modal must include a "How we sized this" section. This is the single most impactful credibility feature. See `design.md` — 24 for the visual template. See `classification-rules.md` — INFERRED derivation chains for the required fields per variable.

### Benchmark Library section on Sources tab (mandatory)

After the Primary Sources table on the Sources tab, add a **Benchmark Library** section listing every published secondary research source used to inform inferred estimates.

- **Eyebrow:** `BENCHMARK LIBRARY`
- **Lede:** *"Published secondary research sources informing the inferred estimates. Each traces to a specific [I#] variable on the Assumptions tab."*
- **Table:** Ref / Source & finding / Informs

This completes the audit chain: **UC modal → variable with I# tag → Assumptions tab (derivation + secondary source) → Sources tab Benchmark Library (full citation).**

---

## In-flight treatment — Mode A (acknowledge) and Mode C (include in analysis)

The skill supports two modes for in-flight items. Mode is captured at intake.

### Mode A — Acknowledge only (legacy default)

In-flight items render as a context section on the Why Now tab. They are NOT in the proposal portfolio, NOT in the financial model, NOT in the charts or table. The dashboard's headline numbers reflect net-new only.

Use when: the audience is a prospect who hasn't shared internal data; the in-flight items are sourced entirely from public research; the Slalom proposition is clearly "net-new on top."

### Mode C — Include in analysis with visual distinction

In-flight items are included in the full financial analysis: financial sizing, Monte Carlo, composite ranking, portfolio table, bubble chart, phasing chart. They carry a visual distinction throughout — see `design.md` — 14 for the Mode C visual treatment table.

The dashboard's headline numbers include in-flight value, but KPI cards distinguish net-new from in-flight: *"28 + 8"* (net-new + in-flight), not just *"36."*

Use when: the audience owns the in-flight work; they want the complete picture; the in-flight items are sourced from client-shared internal documents.

### Intake question

See `intake-checklist.md` — In-flight treatment mode.

---

## Forbidden in every PoV

- **Named exec or named org chart** — there is no specific engagement yet. Don't invent one.
- **Phase 0 dollar figures stated as `TBC`** — always render the order-of-magnitude anchor from `engagement-config.md` — 4 with the explainer tooltip. `TBC` in a financial cell undermines every other number on the tab.
- **Specific validation durations** ("8-week discovery") — leave open.
- **Promises** ("Slalom will deliver $X") — always estimates, always illustrative.
- **Use cases not traceable to AVP source** — every use case must trace to AVP Task Analysis + Use Case Generation rows.
- **"Here is what the portfolio looks like."** — let the visual speak.
- **Engagement Intensity by Phase grid** — omit by default; include only if explicitly requested.
- **Date ranges in phase headers** (Months 0–6, 0–12 months, 12–24 months, 24–36 months) — omit always.
- **"AVP Enhance (EnhanceIQ)"** — use "AVP (AI Value Platform)" in the Sources tab methodology paragraph and on the AVP Analysis tab only. Do not mention AVP in the body of the Summary / Why Now / AI Portfolio / Roadmap tab.
- **Internal AVP terminology in client-facing text** — use client-facing terms (see SKILL.md — Client-facing terminology).
- **"Bundles" or "use case bundles"** — always "use cases" in client-facing content.
- **Pre-tax hero ratios** — always after-tax if a financial ratio is used as the hero.
- **Carriage returns between bold label and inline text** — "Note on scope:" and "Currency note:" stay inline.
- **Disclaimer on tab 1 only** — disclaimer appears on every tab.
- **Scored or quantified sec-eyes without "— ILLUSTRATIVE"** — any sec-eye making a scored or modelled claim carries the suffix.
- **Client-specific moats from prior pursuits** — strip any language tracing to other client work bleeding into a new PoV.
- **Methodology as the headline** — AVP and Slalom methodology are evidence, not the story. The dashboard sells outcomes, not process.

---

## Tab count rule

Seven tabs is the canonical default; five is the tightest acceptable variant. If a build is unusually small (e.g., 8 use cases), make tabs more compact — don't drop them. If unusually large (>18 UCs), consolidate use cases before building, not after. The Assumptions and Sources tabs are never dropped — they are the audit backbone of the PoV.

The AVP Analysis tab is the one optional tab — present only when the user provides one or more value-chain images at intake.

---

## When the user asks to deviate from fixed structure

Push back. The structure is a contract. Surface the tradeoff explicitly: *"That deviation will mean the PoV reads differently from other Slalom PoVs. The advantage is X; the cost is Y. Want me to proceed?"*

Reasonable: cosmetic copy changes, reordering sections within a tab, changing financial metric selection, choosing which matrices appear on the AI Portfolio tab (≥1, ≤5), adjusting the hero framing, switching between the 7-tab default and the 5-tab variant.

Unreasonable: dropping AI Success Patterns, removing the disclaimer, removing the citation system, omitting Monte Carlo for HEAVY-disclaimer engagements, omitting the 10-section per-UC modal architecture (including the Section 7B LOE rationale block), omitting all matrices from the AI Portfolio tab (≥1 matrix is a hard rule), omitting the cost-vs-benefit chart from the Roadmap tab, merging the Assumptions and Sources tabs back into a single tab (the split is part of the canonical contract).
