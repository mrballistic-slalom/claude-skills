# Bundling Logic

The method for turning raw AVP Enhance output into bundled use cases for the PoV.

**Use this when the user hands Claude raw AVP export files** (`eiq_business_function_*.xlsx`) with no pre-bundled UCs. If the user provides bundled UCs already, see the Mode A flow in `SKILL.md` Phase 4 and skip this file. **Hybrid mode** uses this file for the unbundled portion.

---

## Core principle: research-driven, anchor-led

**Bundles are selected by alignment to the Strategic Anchor Framework from Phase 2 — not by AVP scoring.**

The previous version of this file applied a "three-filter method" with AVP's `strategic_fit_score ≥ 75` as a hard filter. That approach produces bundles that read as domain-generic — AVP doesn't know which of the company's stated priorities matter most for the C-suite story. Anchor-led bundling produces bundles that read as company-specific.

AVP's `strategic_fit_score` is consulted **only if the user opted Yes at intake (Question 6 of `intake-checklist.md`)**. When opted in, it acts as a tiebreaker during clustering, not a primary filter.

---

## The source data

Each `eiq_business_function_*.xlsx` file contains three sheets.

### Task Generation
- `wbs_identifier`, `business_unit`, `role` (role-based) or `process` / `subfunction` (process-based)
- `task_title`, `task_description`
- Typically 60-200 tasks per function

### Task Analysis
Same rows as Task Generation, plus 90+ columns of AI-fit scoring.

Key columns for bundling:
- `overall_ai_readiness_score` — **secondary signal, 0-100 scale.** Used to prefer features whose parent tasks are AI-ready.
- `overall_percent_ai_potential` — % of the task AI can plausibly perform
- `overall_reasoning` — narrative on why this score
- `ai_enablers`, `ai_blockers` — JSON arrays informing bundle risk and tech-stack notes

### Use Case Generation
The feature-level use cases, typically 3-5 per task. Each row is one feature.

Key columns:
- `wbs_identifier`, `task_title` (parent task)
- `use_case_name`, `use_case_description` (the feature)
- `technologies` (list of tech stack elements)
- `enhancement_type` — Assist / Anticipate / Augment / Automate / Associate / Agentize
- `level_of_effort` — QUICK_WIN / STANDARD_PROJECT / MAJOR_INITIATIVE
- `differential_risk` — CLEAR_WIN / SOLID_CASE / BALANCED / WEAK_CASE
- `strategic_fit_score` — **opt-in only.** Used as a tiebreaker if Question 6 = Yes.
- `technology_maturity` — MATURE / PROVEN / DEVELOPING / EMERGING

Across typical function exports: 200-700 features per function.

---

## The bundling sequence

### Step 1 — In-flight acknowledgment (NOT in proposal portfolio)

Acceleration plays identified in Phase 2, plus any client-provided AI backlog from intake, become the **in-flight acknowledgment** rendered as a context section in the dashboard (per `structural-rules.md` — In-flight section). They do NOT become Slalom-proposed bundles. Each is sized at the play/initiative level for transparency, but the headline portfolio numbers exclude them.

The Slalom proposal portfolio is 100% net-new use cases — work the client has not publicly disclosed and that isn't in their internal backlog. This separation makes the proposition unambiguous: *"[Client] has X in flight; Slalom proposes Y on top."*

Examples of what feeds the in-flight set:

- A CIO interview confirming a vendor partnership ("we deployed [vendor] to N users with a path to thousands")
- An investor-day slide naming an internal AI platform
- A press release announcing an AI feature launch
- A case study from a named tech partner
- A client-shared backlog of AI initiatives in build, in pilot, or in active planning

For each in-flight initiative:

1. Record name, deployment status, named partners (if any), scope, sized annual value, source citation, and the strategic anchor it most directly supports.
2. Frame in the dashboard as acknowledgment — *"already in deployment"*, *"in build"*, *"announced for launch"* — never as a Slalom proposal.
3. The in-flight set has its own aggregate sub-total in the dashboard's in-flight section, kept separate from the proposal portfolio totals.

If no acceleration plays exist and no client backlog was shared, skip the in-flight section entirely. Don't manufacture entries. Note the absence in the Assumptions tab methodology: *"Client AI work in flight: not surfaced in this PoV; to be discovered during validation."*

### Step 2 — Anchor clustering on the net-new candidate pool (the primary filter)

The candidate pool for bundling **excludes anything overlapping the in-flight set from Step 1**. If an AVP feature corresponds to an initiative the client already has in flight (matched by function and theme), it drops out of the bundling pool — that capability is acknowledged separately, not re-proposed.

For every remaining (net-new) feature in the AVP output:

1. Look at the feature's parent task and sub-function context.
2. Ask: *"Which strategic anchor (from the Phase 2 framework) does this feature most directly serve?"*
3. Tag the feature with the anchor ID.
4. Features that don't map to any anchor go in a "low-anchor-fit" pool — these are candidates for cuts.

Every bundle must trace to **at least one strategic anchor**. Bundles with no anchor mapping fail the credibility test ("we started with your goals, not ours") and should not ship.

### Step 3 — AI-readiness sub-filter

Within each anchor cluster, prefer features whose parent tasks have `overall_ai_readiness_score ≥ 60`. Tasks below 50 are generally excluded unless they're necessary precursors (data foundation, integration scaffolding, governance) for higher-readiness features.

### Step 4 — Strategic-fit tier assignment (research-driven)

Assign each bundle one of four tiers based on **anchor proximity and audience-stated priorities** — not AVP score (unless opted in). Note: deployment status is NOT a tier input — anything already deployed is in the in-flight set per Step 1, not in the proposal portfolio.

| Tier | Definition |
|---|---|
| **HIGHEST** | Direct map to the company's most-named priority (e.g., a CEO quote, a stated FY priority). The headlines for the dashboard. |
| **HIGH** | Strong alignment with stated priorities — a named anchor with a published target or a regulatory/compliance constraint with a public anchor. The strong secondary set. |
| **MEDIUM-HIGH** | Aligned with stated priorities but indirect path — supports a stated priority but not yet a top-named focus area. |
| **MEDIUM** | Operationally valuable but not directly tied to a stated priority. Frame as "supporting" or call out as foundational. |

The skill standardizes these four tier names. Don't invent alternatives ("Critical / Important / Useful / Optional" etc.) — consistency across PoVs is part of the credibility signal.

**If `strategic_fit_score` opt-in (Q6 = Yes):** Use AVP score as a tiebreaker between two candidates that map to the same tier. Prefer the higher AVP score. Do NOT use AVP score to override an anchor-driven tier assignment.

### Step 5 — Functional-challenge sanity check

For each candidate bundle, ask: *"Is this a problem the audience persona has actually told us about, or that the industry discusses openly?"*

Problems to look for:
- Cycle time compression
- Cost-per-unit reduction (with a recognized benchmark)
- Risk or compliance burden
- Customer experience friction
- Capacity constraint
- Decision quality
- Revenue capture
- New capability (previously impossible before AI)

If a high-anchor-fit bundle doesn't map to one of these, fold it into an adjacent bundle or drop. Anchor fit alone isn't sufficient.

### Step 6 — Phase assignment

Assign each bundle to **Phase 1 / 2 / 3** (or Phase 0 if it's foundation work — but Phase 0 is bracketed and TBC, not part of the use case portfolio).

| Bundle profile | Phase |
|---|---|
| Dominated by QUICK_WIN features, MATURE tech, deployable now | **Phase 1** — deploy Year 0 |
| Mixed LOE, depends on Phase 1 outputs being live, MATURE/PROVEN tech | **Phase 2** — deploy Year 1 |
| MAJOR_INITIATIVE features, depends on platform migration at scale, deeper workflow redesign | **Phase 3** — deploy Year 2 |

The portfolio must show the **compounding curve**: Phase 3 bundles should have the highest annual benefit despite (and because of) longer paybacks. If your bundles don't produce this shape, revisit step 5 — Phase 3 use cases should represent the deepest function reshaping, which typically produces larger benefits than edge optimization.

### Step 7 — Track candidates that didn't make the cut

Throughout bundling, every candidate considered seriously but cut from the proposal must be recorded with:

- **id** (UC-XXX)
- **candidate name**
- **source function** (F#)
- **cut reason** (1 sentence; specific, not generic)

Cut reasons must be substantive — for example: *"Overlaps with UC-Y; absorbed,"* *"Lower anchor fit vs. UC-Y,"* *"Already in the client's in-flight set; Slalom-identified scope too narrow to stand alone,"* *"Belongs in Phase 0 foundation work."* Generic reasons (*"not strong enough,"* *"didn't fit"*) fail the credibility test.

This list feeds the AI Portfolio tab "Considered but cut" panel per `structural-rules.md`.

---

## Bundle composition rules

### Target counts — two-stage approach

**Stage 1 — Broad pool (Phase 3):** Target ~50 anchor-aligned candidates. Cast wide. Every credible candidate that passes the anchor, readiness, and sanity-check filters enters the pool. If AVP output supports 60, take 60. If it supports 35, take 35. The point is to give Monte Carlo enough candidates to rank meaningfully. Don't artificially cap at this stage.

**Stage 2 — Final portfolio (Phase 7, post-MC downselection):** The composite MC rank drives the cut to the user's target:

- **Tight (8-12)** — focused, executive-ready
- **Standard (12-18)** — comprehensive coverage
- **Comprehensive (18-25)** — appropriate when the source AVP run covers many operations and the audience expects breadth

Candidates that don't survive downselection become "Evaluated but deprioritized" — fully sized and MC-tested, rendered in a distinct panel on the AI Portfolio tab (see `structural-rules.md` — Evaluated but deprioritized panel).

If the broad pool is smaller than 25, the user may choose to skip formal downselection and carry the full pool forward — but MC still runs on all candidates regardless.

### Each bundle must have

Bundles are net-new by definition (in-flight items live in a separate top-level data structure — see — In-flight data model below). Every bundle must have:

- **Name** — 40-60 chars, business-value language (not technique names). "Direct booking acceleration & reservations co-pilot" not "ML personalization for booking funnel."
- **Description** — 60-120 words tied to a recognizable functional challenge.
- **Strategic-fit tier** — HIGHEST / HIGH / MEDIUM-HIGH / MEDIUM
- **Anchors served** — list of strategic anchor IDs (≥1 required)
- **Constituent features** — list of Use Case Generation rows by `wbs_identifier`
- **Parent tasks** — set of unique tasks the features came from
- **LOE tier** — modal LOE across constituent features
- **Phase** — 1 / 2 / 3
- **Technologies** — aggregated from features' `technologies` fields, plus any client-named partner tech when public
- **Benefit class** — one of Hard cost reduction / Productivity savings / Cost avoidance / Revenue assurance / Incremental revenue (see `benefit-classification.md`)
- **Public-language hygiene** — don't reference company-internal codenames the company doesn't publicly use. Use generic platform language (see `primary-source-research.md` — Public-language hygiene lists).

### In-flight data model (separate from bundles)

In-flight initiatives are stored as a top-level structure, NOT as bundles. Each in-flight initiative has:

- **id** (e.g., `INF-001`)
- **name**
- **deployment_status** — in production / in deployment / active collaboration / in build / announced for launch
- **named_partners** (if any)
- **scope** (1-line description)
- **anchor_mapping** — which strategic anchor(s) it supports
- **sized_annual_value** (sized for transparency; not in proposal portfolio totals)
- **source_citation(s)** — `[S#]` references for public-source items; `[CLIENT_BACKLOG]` tag for client-shared items

### Financial parameters per bundle

- **One-time investment** — sum of `estimated_cost` across constituent features, refined with engineering judgment, ×1.25 enablement surcharge per `financial-model.md`.
- **Annual ongoing** — base ops + compute surcharge by LOE + $0.03M/yr enablement maintenance.
- **Annual benefit** — sized against company financials and stated targets. Use the company's own scale (revenue, headcount, member count, property count, etc.) rather than industry generic.

Apply the classification discipline from `references/classification-rules.md` to every financial line.

---

## Citation system within bundles

Every quantitative claim in a bundle's basis text gets a citation reference per the system in `structural-rules.md` — Citation IDs. Conventions:

- `[S#]` — primary source (10-K, earnings transcript, press release, regulatory filing)
- `[B#]` — benchmark (consulting research, industry association)
- `[I#]` — inferred (Slalom reasoning, modeled assumption)

**Citation routing rule:**
- `[S#]` and `[B#]` body refs → Sources tab + scroll to the matching row
- `[I#]` body refs → Assumptions tab + scroll to the matching row

Each bundle's transparency table (Modal section "How we sized") cites every row.

---

## Tracing to source

For every bundle, maintain a traceability record:

```
bundle_id: UC-XXX
strategic_fit_tier: HIGHEST | HIGH | MEDIUM-HIGH | MEDIUM
anchors: [anchor_id_list]
source_function: [BU name]
parent_tasks: [wbs_identifier list]
constituent_features: [use_case_name list with wbs_identifiers]
avg_task_ai_readiness: X.X
avg_feature_strategic_fit: X.X  (recorded for QA, not used for tier unless Q6 = Yes)
```

(All bundles are net-new by definition. There is no `acceleration_play` or `slalom_incremental_share` field — anything pre-existing is in the in-flight set, not a bundle.)

The QA checklist's AVP trace check randomly samples 2-3 bundles and verifies the trace holds. If it doesn't, the bundle violates the "AVP-rooted" contract and must be revisited.

---

## Anti-patterns

- **Absorbing an in-flight client capability into a Slalom bundle as a "scale-out play."** This conflates client trajectory with Slalom proposal and reads as confused or claim-jumping. Acknowledge the client's work separately in the in-flight section; propose net-new on top.
- **Selecting bundles by AVP score alone.** Anchor fit is the primary filter; AVP score is opt-in tiebreaker only.
- **Bundles with no anchor.** Every bundle traces to ≥1 anchor. No exceptions.
- **Manufactured in-flight items.** Don't label an initiative as "in deployment" or "in build" unless the client has publicly disclosed it OR shared it as backlog. Embellishment kills credibility.
- **Tier inflation.** Most bundles are HIGH or MEDIUM-HIGH. Use HIGHEST sparingly — only for direct CEO-quote-level alignment to the company's most-named priority.
- **Public-language violations.** If the company uses internal codenames the public doesn't see (e.g., a project name that only appears in employee documentation), don't use it in the dashboard. Use the generic platform language.
- **Cutting the broad pool early.** Phase 3 targets ~50 candidates intentionally. Trimming to 15 before MC runs defeats the purpose — MC needs a broad field to rank meaningfully. Let Phase 7 do the cutting.
- **Treating the composite rank as absolute.** The rank is a recommendation. The user may override for strategic reasons — a lower-ranked UC that the audience cares about should survive. Document every override.
- **Bundling across all 90+ Task Analysis columns.** Anchor → AI readiness → tier → phase. Five steps. Don't multi-attribute optimize.
- **Claude inventing features.** If the bundle mentions a capability that isn't in any constituent feature's `use_case_name` or `use_case_description`, stop. That's no longer AVP-rooted.

---

## Quick cheat sheet

```
1. Load AVP file(s) → pandas
2. Pull Phase 2 strategic anchor framework + acceleration play list + hygiene lists + (optional) client AI backlog
3. Build the in-flight set (acceleration plays + client backlog) → separate data structure, NOT bundles
4. Net-new candidate pool = AVP features minus anything overlapping in-flight items
5. For each net-new feature → tag with serving anchor; drop low-anchor-fit
6. Within anchor clusters → prefer features with task readiness ≥ 60
7. Compose bundles by anchor cluster + functional challenge sanity check (track candidates considered but cut)
8. Assign tier (HIGHEST/HIGH/MEDIUM-HIGH/MEDIUM) by anchor proximity to stated priorities
9. (Optional, if Q6 = Yes) use AVP strategic_fit_score as tiebreaker
10. Assign LOE / phase (1/2/3) / benefit class
11. TARGET: ~50 candidates in the broad pool — present to user for review
12. Full financial sizing on all ~50 (Phase 5)
13. Monte Carlo on all ~50 (Phase 6) → composite rank
14. Downselect to 8-25 using composite rank (Phase 7) — user confirms
15. Candidates that don't survive → "Evaluated but deprioritized" panel
16. Inherit financials from AVP, refine with company-scale benchmarks
17. Classify every line (BENCHMARK / INFERRED), cite per [S#]/[B#]/[I#] system
18. Record trace (anchors + parent_tasks + constituent_features for every bundle)
19. Present final portfolio to user for confirmation before rendering HTML
```
