---
name: avp-pov-builder
version: "3.4"
updated: "2026-05-28"
description: "Builds Slalom's PoV on AI Transformation — a standalone HTML dashboard making a provocative case for AI at a client. Takes AVP Enhance outputs (Task Analysis + Use Case Generation) and renders an industry-agnostic dashboard. Pairs upstream with `avp-input-builder`; runs standalone if AVP outputs exist. Two-stage portfolio downselect from ~50 candidates to 8-25 via 10K Monte Carlo; renders an optional Portfolio View Toggle (Prioritized ↔ All Evaluated) when the broad pool exceeds the final portfolio. Canonical 7-tab structure (Summary · Why Now · AI Portfolio · AVP Analysis · Roadmap · Assumptions · Sources); Phase 8.5 hero-lock + decisions-log artifacts ship every build. Intake captures industry profile (9 sectors + custom), cost mode, and design variant (canonical default; Multifile/Extended overlays). Supports nonprofits, government, cooperatives. Use when asked to build a Slalom PoV on AI Transformation, a prospecting AI dashboard, or a provocative AI transformation case for a client."
---

# Slalom PoV on AI Transformation — Skill

This skill takes **AVP Enhance output** for a specific client or domain and builds a standalone, proactive HTML dashboard that makes a provocative, defensible case for where AI can transform that business.

**The dashboard is a provocation, not a proposal.** Its job is to demonstrate that Slalom has already thought harder about this client's AI opportunity than they have — making them want to fund the validation conversation. It does not wait to be invited.

**Core principle: AVP-rooted or it does not run.** Every use case draws from real AVP Enhance output — Task Analysis and Use Case Generation exports. Claude does not invent use cases from benchmarks alone. The platform is referred to throughout as **AVP (AI Value Platform)** — never as "AVP Enhance (EnhanceIQ)". When users provide raw AVP export files, Claude bundles features using `references/bundling-logic.md`. When users provide pre-bundled use cases, Claude validates and renders.

**Disclaimer is a feature, not a footer.** The dashboard says clearly it was built without the client's proprietary data and that financial estimates are illustrative pending validation. That honesty is the implicit pitch: *"We built this using AVP methodology applied to your domain. Now let's apply it to your reality."* The disclaimer appears on **every tab** — not just tab 1.

---

## How this pairs with `avp-input-builder`

This skill is one half of a paired Slalom workflow for AI PoV work on AVP:

- **`avp-input-builder`** — Builds the inputs AVP needs: Demo Brief, client research, Business Function setup, Enhance Excel, Business Context Questions. Stops at the AVP Enhance hand-off.
- **`avp-pov-builder`** *(this skill)* — Takes the resulting AVP Enhance outputs and builds Slalom's PoV on AI Transformation: a standalone HTML dashboard making a provocative, defensible case for the client.

**The sequence when paired:** `avp-input-builder` → *user runs AVP Enhance externally* → AVP Enhance exports → `avp-pov-builder` → HTML dashboard.

**They don't have to run together.** Use this skill standalone when you already have AVP Enhance outputs in hand and just need the dashboard. Use `avp-input-builder` standalone when you only need AVP intake artifacts (e.g., a Calculate-led demo). Most of the time, though, they run as a pair.

**Artifacts that carry across.** When `avp-input-builder` ran first, the Demo Brief, company description, financial parameters (discount/tax/hurdle), audience context, and business-function inventory already exist. At Phase 1 intake here, ask the user to paste them in or point to where they're saved — don't re-elicit.

---

## When to use this skill

Trigger on requests like:
- "Build a Slalom PoV on AI Transformation for [client/company]"
- "Turn these AVP exports into a PoV for [X]"
- "Make a provocative AI transformation case for [X]"
- "Build a prospecting AI dashboard from this AVP output"
- "Build a Slalom PoV on AI for [client]"

**Do not use this skill for:**
- AVP intake artifacts (Demo Brief, Business Function setup, Enhance Excel) when AVP Enhance hasn't yet run → use `avp-input-builder` first
- AVP Calculate output dashboards for a specific client → use `avp-dashboard-builder`
- Cold-start inference with no AVP output available — this skill requires AVP Enhance output as input

---

## Required input

**At least one of the following:**

- **AVP Enhance business function export** — the `eiq_business_function_*.xlsx` file produced by running Enhance on a business function. Contains three sheets: Task Generation, Task Analysis, Use Case Generation. Multiple files are fine (one per function). This is **Mode B — Claude bundles**.

- **Pre-bundled use case list** — the user has already clustered AVP features into bundled use cases. Must include: bundle name, description, constituent features (optional but useful), LOE, risk, tech stack, and rough financial parameters. This is **Mode A — user provides bundles**.

- **Both** — some pre-bundled, some raw. Claude uses Mode A for the pre-bundled material and Mode B for the rest.

**Optional — client AI backlog.** If the client has shared an internal list of AI work already underway or planned, include it. The intake checklist asks for it. Combined with public-source acceleration plays, it forms the "in flight" acknowledgment section. The Slalom proposal portfolio is always net-new use cases on top.

**If the user has none of these,** stop and say so: *"This skill requires AVP Enhance output as its source of truth for use cases. If you don't have AVP output, let's run Enhance first — or use a different deliverable type."* Do not proceed on topic alone.

---

## Workflow

### Phase 1 — Intake

Walk the user through `references/intake-checklist.md`. The first question is always: *"What AVP Enhance output do you have for me to work with?"* — this determines mode (A, B, or hybrid) and gates everything downstream.

**Was `avp-input-builder` run first?** If yes, ask the user to share its outputs — Demo Brief, company description, financial parameters (discount/tax/hurdle), audience context, business-function inventory. Reuse all of it rather than re-eliciting. If no, proceed with the standard Phase 1 intake.

**Capture the engagement config in parallel.** Walk the user through `references/engagement-config.md` — 12 template — revenue tier, **industry profile (REQUIRED — pick from — 2a; no silent default)**, industry composite (WACC, hurdle rate, EBITDA margin or sector proxy), financial structure (for-profit / nonprofit / government / cooperative per — 13), Phase 0 dollar anchor, existing tech stack baseline, strategic anchors A1–A8 (filled after Phase 2 research), heatmap stops (read from supplied AVP image), in-flight statuses, function color palette, in-scope functions and acronyms. Save as `engagement-config-{client}.md` alongside the AVP exports. The skill will not start Phase 9 (build the HTML) without a complete engagement config — including an explicitly selected industry profile.

**The skill is industry-agnostic by design.** All sector economics live in the engagement config (Layer 2), not in the universal rules (Layer 1). The intake forces the user to pick an industry profile so the financial composite reflects the actual client sector — banking, insurance, SaaS, retail, hospitality, telco, industrial, energy/utilities, or custom (see `engagement-config.md` — 2a). Non-standard structures (nonprofits, government, cooperatives) are accommodated via the — 13 financial-structure override layered on top of the sector profile. A careless run on a non-industrial client cannot silently fall through to industrial mid-cap — Q5c of the intake refuses to proceed without a profile.

Other intake inputs:
- Client or domain (who is this for)
- Pattern type (process / industry / function / company)
- Target audience (prospect persona)
- Supporting documentation beyond AVP output
- Competitive or market context the user wants woven in
- **Use AVP `strategic_fit_score` as a bundling input?** Default: **No** — strategic fit is derived from the Phase 2 anchor framework. Set Yes only if research is thin or anchors are ambiguous and the user wants AVP scoring as a tiebreaker.
- **Tab structure** — present the canonical menu: 7-tab default (Summary · Why Now · AI Portfolio · AVP Analysis · Roadmap · Assumptions · Sources) or 5-tab tighter variant (Summary · AI Portfolio with Why Now folded in · Roadmap · Assumptions · Sources). The AVP Analysis tab is optional regardless of variant — depends on whether the user provides value-chain images at intake (Question 10). The mandatory minimum is Summary + AI Portfolio + Roadmap + Assumptions + Sources.
- **Design variant** — Question 22. Default is canonical (per `references/design.md` + `references/golden-master.md`). Named overlays available: Multifile, Extended (see `references/design-variants/`). Custom overlays can be added at intake when a new variant is genuinely needed; canonical otherwise.
- **Localization** — make a guess from the client's HQ (US English / US$ for U.S. companies; Canadian / British / Australian conventions for non-U.S.) and confirm with the user before proceeding. Don't infer silently.
- **Output path** — ask where the final HTML should be written. Don't assume `/mnt/user-data/outputs/` — that's a Claude.ai pattern. Default for local builds: same directory as the input materials.
- **Cost mode** — Standard / **Optimized (default)** / Full-fidelity. Controls revision economics: in Optimized mode the build uses edit-in-place for revisions and only bumps the version number at named milestones (first complete render, after user review, final). Full-fidelity is for high-stakes client-facing runs where the user wants every iteration preserved. See the **Cost mode** section below for the full rules and the optional opt-in levers.

### Phase 2 — Primary Source Research + Strategic Anchor Framework

**Runs before bundling, every time.** Read `references/primary-source-research.md`.

**For publicly traded companies:** Pull 10-K, 10-Q, earnings call transcripts, investor day presentations, and recent press releases. Build a **Strategic Anchor Framework** — a structured inventory of the company's publicly stated strategic objectives, financial targets, and operational priorities. Every use case in the portfolio will tag to one or more anchors. These anchors become the backbone of the "Your goals. Our analysis." section on Tab 1.

**For privately held companies:** Identify 2–3 public comparables and pull the same filings. Supplement with web research for press coverage, industry awards, leadership interviews, and trade publications. The user is a critical source — ask what they know about the company's stated priorities, growth trajectory, and pain points. Build the strategic anchor framework from the combination of comp analysis, web research, and user-provided context.

**In all cases:** The strategic anchor framework maps every use case to a stated business objective. It is the primary credibility signal — it tells the audience *"we started with your goals, not ours."* The framework includes source citations for every anchor. **The anchors — not AVP scores — are the primary input to bundle selection in Phase 3.**

**Anchor specificity is a hard gate** — every anchor passes the specificity test from `references/anchor-specificity.md`: mentally swap the client's name for "Acme Corp." If the section still makes sense, the anchor is too generic and must be rewritten with named specifics (docket number, named target, dated event, named asset, named legislation). Generic anchors that could apply to any peer in the industry fail the credibility bar and force expensive rewrites later — catch them at Phase 2, not after render.

**Three additional research outputs (mandatory):**

1. **Acceleration play discovery.** Identify any AI capability the client has *publicly identified as deployed, in deployment, in build, or announced for launch* — named programs, named partners, named pilots. Examples: a CIO interview confirming a vendor partnership, an investor-day slide naming an internal AI platform, a press release announcing an AI feature launch. These items feed the dashboard's **in-flight acknowledgment section** (per `bundling-logic.md` — Step 1 and `structural-rules.md` — In-flight section), alongside any client-provided AI backlog from intake. They are NOT Slalom-proposed bundles — the proposal portfolio is always net-new on top.

2. **Public-language hygiene lists.** Produce two lists for the bundler and writer to use:
   - **Use these names** — partners, products, programs, leaders that ARE in primary disclosures.
   - **Avoid these names** — internal-but-not-public terminology that bleeds in from training-data recall (e.g., codenames the company doesn't use externally).
   The "Avoid" list prevents the dashboard from referencing systems by names the company doesn't publicly use.

3. **Freshness check.** Every quantitative number cited from primary sources should be from filings published within the last 12 months. If older, flag it explicitly. Catches stale figures (e.g., outdated member counts, prior-period revenue) before they reach the dashboard.

Classification tags: `CLIENT_DATA` / `BENCHMARK` / `INFERRED`. Comp-derived parameters tagged `(CLIENT_DATA: COMP:{ticker})`.

### Phase 3 — Bundling (Mode B and hybrid) — BROAD POOL (~50 candidates)

Read `references/bundling-logic.md`. Bundling is **research-driven by default** — the strategic anchor framework from Phase 2 is the primary input. AVP's `strategic_fit_score` is consulted **only if the user opted Yes** at intake.

**Phase 3 intentionally casts wide.** The target is ~50 anchor-aligned bundled use cases — every credible candidate that passes the anchor, readiness, and sanity-check filters. This is NOT the final portfolio. Downselection to 8–25 happens after full financial sizing and Monte Carlo analysis (Phase 7). The purpose of the broad pool is to give MC enough candidates to rank meaningfully — cutting early wastes information.

**Net-new vs. in-flight separation.** Acceleration plays identified in Phase 2 (publicly disclosed AI work the client has named) and any client AI backlog shared at intake do **NOT** become bundles in the Slalom proposal portfolio. They feed the dashboard's "What [client] has in flight" acknowledgment section instead. Slalom's proposal bundles are 100% net-new — work the client has not publicly disclosed and that isn't in their internal backlog.

The bundling flow:

1. **Identify the in-flight set.** Acceleration plays + any client-provided AI backlog form the in-flight acknowledgment, rendered as a context section in the dashboard. Sized at the play/initiative level for transparency. NOT in the proposal portfolio.
2. **Anchor-driven clustering on the net-new candidate pool.** Working only with AVP features that don't overlap the in-flight set, cluster by which strategic anchor each feature supports. Every bundle traces to ≥1 anchor.
3. **AI-readiness filter (Task Analysis).** Within each anchor cluster, prefer features tied to tasks with `overall_ai_readiness_score` ≥ 60.
4. **Strategic-fit tier assignment.** Bundle strategic-fit tier (HIGHEST / HIGH / MEDIUM-HIGH / MEDIUM) is derived from anchor proximity and audience-stated priorities — not AVP score (unless opted in).
5. **Functional-challenge sanity check.** Every bundle must tie to a recognizable problem in the domain.

Present the full ~50-candidate broad pool to the user for review before proceeding to financial sizing. The user may flag obvious removes at this stage, but the primary downselection happens after MC (Phase 7). The proposition is unambiguous: *"[Client] has X in flight; Slalom proposes Y on top."*

### Phase 4 — Bundle validation (Mode A only)

Validate every bundle has: name, description, feature references or reasoning chain, LOE tier, risk tier, tech stack, financial parameters. Flag and fill gaps.

### Phase 5 — Financial sizing (full treatment on all ~50 candidates)

Apply classification discipline from `references/classification-rules.md`. Every UC financial line is classified (BENCHMARK / INFERRED). Use computation logic from `references/financial-model.md`. **All ~50 candidates from the broad pool receive full financial treatment** — benefit classification, cost narrative, phased investment — so that Monte Carlo has real numbers to rank against.

**Financial metric selection:** Before rendering, recommend to the user which financial metrics should feature prominently based on audience and data quality. See `references/financial-model.md` — Financial Metric Selection for the decision framework. The choice of headline metric affects what appears in the hero, the KPI strip, the Tab 2 chart axes, and the Tab 3 phase cards.

**Portfolio realization rate (required question — ask before computing hero figures).** Ask: *"Should the headline numbers be shown at full portfolio value (100%), or modeled at a conservative realization rate — e.g., 60% to reflect typical delivery friction, scope change, and adoption variance? If a realization rate applies, it appears in the `*` caveat on the hero and sets all starred figures."* Present both the gross figure and the realization-adjusted figure so the user can see the difference before deciding. Capture the chosen rate in the engagement config. The default is **60% for HEAVY disclaimer mode**; 100% for STANDARD or TIGHT. Every metric marked `*` in the hero, KPI strip, and phase chevrons must be calculated at the agreed rate — never mix realization-adjusted and gross figures in the same `*` tier without an explicit label distinguishing them.

**Benefit classification (required):** Every UC's annual benefit must classify into one of five detail classes — Hard cost reduction / Productivity savings / Cost avoidance / Revenue assurance / Incremental revenue — and roll up to three executive buckets (Cost-side savings · Revenue assurance · Incremental revenue). See `references/benefit-classification.md`. Without this, the headline financial number loses CFO-defensibility.

**INFERRED derivation chains (required):** Every INFERRED line must carry a derivation chain — what was inferred from, what the chain of reasoning was, what comparable was used. A bare `(INFERRED)` tag without a "where does this come from?" chain fails the audit. See `references/classification-rules.md` — INFERRED derivation chains. The chain renders in the per-UC modal's Section 7A (How we sized the annual benefit) and in the Assumptions tab I-rows.

**Phase 0 financial treatment:** Phase 0 (foundation work) is always rendered with the engagement's order-of-magnitude anchor (per `engagement-config.md` — 4 — e.g., `~$8–12M*` for a $7B archetype), **never as `TBC`** and **never included in portfolio NPV, annual benefit, or hero totals**. Phase 0 is a parallel-track shared platform investment scoped during validation; rolling it into the portfolio total bloats the headline and undercuts credibility when the true Phase 0 cost surfaces later.

**Time horizon decision:** Default Monte Carlo and NPV horizon is **5 years**. Switch to **7 years** if (Phase 3 implementation cost ≥ 30% of portfolio total) AND (Phase 3 is >50% MAJOR_INITIATIVE LOE tier). Rationale: a 5-year horizon truncates the benefits of Phase 3 use cases (deploy Year 2 + 5-year ramp = full benefits captured at Year 7). For function-reshape portfolios with Phase 3 weight, the 5-year horizon produces misleadingly negative Phase 3 NPVs. See `references/financial-model.md` — Time horizon — decision rule.

**Cost narrative (required):** Express investment as phased one-time + ongoing + cumulative — never a single "total investment" number. The Roadmap tab carries a cumulative cost-vs-benefit chart with crossover annotation (fixed section) and a cost breakdown table in the Overview view. See `references/financial-model.md` — Cost narrative.

**Relative LOE percentile (required, distinct from the LOE tier):** Compute a 0–100 relative LOE percentile across the broad pool for every bundle, weighting implementation cost, change burden, tech maturity, data readiness, and regulatory/org friction (default weights and methodology in `references/portfolio-matrices.md` — The relative LOE percentile). The percentile is the matrix-axis measure; the categorical LOE tier (Quick Win / Standard / Major Initiative) is unchanged and continues to drive ramp curves and compute surcharges in `financial-model.md`. Capture LOE rationale + assumptions per bundle now — they render in Section 7B of the per-UC modal at Phase 9.

### Phase 6 — Monte Carlo sensitivity (on all ~50 candidates)

For HEAVY-disclaimer engagements (the default), run a 10,000-trial Monte Carlo following `references/monte-carlo.md` **on the full broad pool (~50 candidates)**. Distributions cover annual benefit, implementation cost, ongoing cost, ramp realization, hurdle rate, and tax rate. Output P10/P50/P90 ranges per UC and portfolio plus probability metrics (probability of clearing the client's stated target, probability of positive NPV, probability of acceptable payback).

**Composite ranking (required).** After MC completes, compute a composite rank score for every candidate using the methodology in `references/monte-carlo.md` — Composite ranking for downselection. This rank is the primary input to Phase 7.

Always carry the "sensitivity, not added precision" caveat — MC on inferred inputs sharpens variance, not rigour.

### Phase 6.5 — Matrix selection (audience-driven storytelling for the AI Portfolio tab)

Every PoV ships **at least one matrix on the AI Portfolio tab; up to five.** Read `references/portfolio-matrices.md`. The matrix block is the storytelling spine of the AI Portfolio tab — the right axis pair (or pairs) varies by audience, industry, and which dimensions the MC results actually discriminate on.

The selection happens here, **after Phase 6 MC**, because some axis pairs go dead if the underlying dimension doesn't discriminate (e.g., every candidate paying back in 14–18 months kills "Break-Even" as an axis) — only MC tells you that.

The flow:

1. **Compute discrimination per candidate axis** — IQR across the broad pool for each axis (annual benefit, NPV, payback, break-even, EBITDA impact, anchor strength, relative LOE percentile, P(NPV>0)). Axes with IQR < 20% of median are flagged as low-discrimination.
2. **Build the recommended shortlist** — 2–3 matrices from the audience → matrix table in `portfolio-matrices.md`, filtered by the discrimination check, with rationale.
3. **Present to user** with the recommended primary, secondary, optional, and any demotions ("EBITDA impact dropped — IQR is 12% of median").
4. **User decides** which matrices to include (≥1, ≤5) and the rendering order.

The matrices use the **relative LOE percentile** computed in Phase 5 as the LOE axis (not the categorical LOE tier). Axes follow **natural orientation** — short payback / low LOE / fast break-even sit on the left, not the right. The **win quadrant therefore varies by matrix** (top-left or top-right depending on whether "less" or "more" is good on each axis); each matrix labels its win quadrant explicitly per `portfolio-matrices.md`. All matrices carry a **mandatory classification overlay** — bundles with ≥1 INFERRED line render with a striped/dashed border; all-BENCHMARK/CLIENT_DATA render with a solid border. Without the overlay, a "fast payback, high benefit" placement based on inferred inputs is a credibility landmine.

### Phase 7 — Downselection (MC-driven, ~50 → 8–25)

**This is where the portfolio gets shaped.** Using the composite rank from Phase 6, downselect the ~50-candidate broad pool to 8–25 use cases that form the final proposal portfolio.

The downselection protocol (see `references/monte-carlo.md` — Downselection protocol):

1. **Rank all ~50 candidates by composite score** (descending). Present the ranked list to the user with MC headline metrics per candidate.
2. **Apply the user's target range (8–25).** The intake question (Q17) sets the target. The composite rank determines who's in and who's out. Natural breaks in the ranking often suggest where to draw the line.
3. **User-guided adjustment.** The ranked list is a recommendation, not a decree. The user may override: pull a lower-ranked candidate up for strategic reasons (audience cares about it), or push a high-ranked candidate down (domain knowledge says it won't land). Every override gets documented in the Assumptions tab.
4. **Candidates that don't survive become "Evaluated but deprioritized"** — a distinct panel on the AI Portfolio tab (see `structural-rules.md` — Evaluated but deprioritized panel). These are NOT the same as Phase 3 "considered but cut" candidates — they were fully sized and MC-tested, which gives them a different evidentiary status.

**Persist BOTH lists to `mc_results.json`.** Write `final_list` (the 8–25 portfolio) AND `deprio` (the evaluated-but-deprioritized candidates) — not just the final. Phase 9 needs both pools to wire the **Portfolio View Toggle** (see `references/portfolio-view-toggle.md`), which exposes the full broad-pool analysis as a first-class view on the AI Portfolio tab. Without the deprio list persisted, the toggle has nothing to render in the "All Evaluated" state.

Present the final portfolio to the user for confirmation before rendering HTML.

Per-UC modals for the final portfolio carry the MC range bars and a P(NPV>0) badge. The Assumptions tab carries the portfolio confidence section.

### Phase 8 — AI SUCCESS PATTERNS mapping

Read `references/four-winning-patterns.md`. Map all four patterns to specifics for the client/domain. Always all four. Each gets a concrete "In [client/topic]:" callout.

### Phase 8.5 — Hero lock (gated)

Read `references/hero-lock.md`. Before Phase 9 renders the ~3,000-line HTML, present a **one-screen text preview** of the hero composition to the user and **wait for an explicit lock**. The preview covers all five hero components: title, tagline, big-one, the 2×3 supporting KPI strip, and the Phase 0/1/2/3 strip (auto-derived from the locked portfolio). The preview must also state the realization rate in force (e.g., *"All `*` figures modeled at 60% portfolio realization"*) so the user can confirm or change it before the HTML is rendered.

**This is a hard gate.** Phase 9 does not start without an explicit "lock it" / "y" / equivalent from the user. The lock is the v2.4 answer to the most expensive iteration pattern observed historically: title/tagline/big-one churn *after* the first full render. Locking pre-render moves that churn into cheap text iteration instead of full HTML re-renders.

When the user locks, **write the locked hero to the decisions log** (`decisions-{client}.md` — 1 — Hero lock) per `references/decisions-log.md`. The lock survives session boundaries.

When the user wants to change the hero **after** Phase 9 has rendered, return to Phase 8.5, present the updated preview, get a new lock, then revise the HTML — edit-in-place in Optimized cost mode, new version file in Full-fidelity.

### Phase 9 — Build the HTML

---

#### The transformation contract

**Your Phase 9 output IS `references/build-skeleton.html` with engagement-specific content filled in.** You are an editor, not a generator. Every structural element — DOCTYPE declaration, `<head>` block, Chart.js `<script>` tag, `<style>` block, nav bar, tab button row, all 7 tab panels, modal overlay, glossary panel, and all closing tags — comes directly from the skeleton. You do not write these from scratch; you reproduce them with client content substituted inside them.

**The skeleton as of v3.0 contains 276 `{{PLACEHOLDER}}` markers** — one for every client-specific injection point. Your job is to fill every marker. The QA script hard-fails on any `{{PLACEHOLDER}}` left in the final output.

**The complete list of things that originate with you — and nothing else:**
- Client title, tagline, hero big-one, and 2×3 KPI strip (locked at Phase 8.5)
- Use case names, descriptions, financial figures, and phase assignments (from downselect output)
- Engagement JSON block (replaces `{{ENGAGEMENT_DATA_START}}` / `{{ENGAGEMENT_DATA_END}}` block)
- Chart.js data arrays (`{{ROADMAP_CUM_BENEFIT}}`, `{{ROADMAP_CUM_COST}}`)
- Source citation rows and assumption rows (S#, B#, I# tables)
- Engagement-specific anchor text and strategic narrative

**Everything else — structure, CSS, JS, component patterns, the attribution footer — comes from the skeleton.**

---

#### Read the guide. Use the helper. The skeleton is data-driven (v3.0).

As of v3.0 the skeleton is data-driven. UC tiles, UC table rows, matrix bubbles, and Assumptions table rows all render from a single `<script id="portfolio-data">` JSON block at `DOMContentLoaded` — the skeleton's HTML for these areas is empty containers populated by JS. UC count is flexible; matrix bubble positions live in data.

**Step 1.** Read `references/skeleton-transformer-guide.md` end to end. It documents the engagement-data JSON shape, the `{{}}` inline placeholders, the `HERO` section marker, the CSS class canon (~150 classes), and the JS function inventory (~30 functions).

**Step 2.** Use `references/transform.py`. The `Skeleton` class exposes:

```python
import sys; sys.path.insert(0, 'references')
from transform import Skeleton

sk = Skeleton('references/build-skeleton.html')
sk.set_engagement_data(engagement_data_dict)            # → renders all UC content via JS
sk.fill_inline('PAGE_TITLE', '...')
sk.fill_inline('NAV_TITLE', '...')
sk.fill_inline('CLIENT_NAME', 'Client Name')             # appears 19× in narrative
sk.fill_inline('ENGAGEMENT_DOMAIN', 'Industry/Domain')
sk.fill_section('HERO', hero_html)
sk.write('output/{slug}_AI_Portfolio_v1.html')
```

`Skeleton.write()` enforces the v3.0 contract:
- Refuses to write if any `{{PLACEHOLDER}}` is unfilled
- Refuses to write if any required section (`HERO`) was not filled
- Refuses to write if `set_engagement_data()` was never called
- Refuses to write if any filter chip is wrapped in `<!-- -->` (the v2.7/v2.8 self-repair suppression failure mode)
- Refuses to write if a `portfolio-toggle-suppressed` comment exists
- Refuses to write if output > 1.8× skeleton (generation canary — v3.0 expects ratio ~1.0× because UC content renders from data, not HTML)
- Refuses `fill_section` content that contains its own `{{NAME_START}}/{{NAME_END}}` markers (marker leak-back)
- Refuses empty `fill_section` content
- Refuses `fill_section` / `fill_inline` calls with typo'd names

**Narrative copy:** The skeleton ships with Acme Industries / Manufacturing sample content as design reference (anchor cards, market trends, value chain steps, source citations, etc.). Customize these per engagement via the `Edit` tool (Claude Code) or post-`write()` `html.replace` operations. Narrative content is intentionally NOT a `{{}}` placeholder so you can write engagement-fit prose with full HTML formatting.

**What you do not do:**
- Do not write `open('build-skeleton.html')` followed by `re.sub()` against the full document string. Use `Skeleton`.
- Do not write a function called `transform_*`, `build_*`, or `generate_*`. You are an editor, not a generator.
- Do not construct UC HTML in Python — UC tiles/rows/bubbles render from the engagement-data JSON automatically. If you find yourself writing `<div class="uc-tile">` in fill_section arguments, you are bypassing the data-driven path.
- Do not write `html = """<!DOCTYPE html>..."""` anywhere. That is recreating from memory.

**Claude Code path (has shell):** `cp references/build-skeleton.html output/{slug}_AI_Portfolio_v1.html`, then use the `Edit` tool on the output file. Replace `{{ENGAGEMENT_DATA_JSON}}` with the serialized engagement data dict, replace inline `{{}}` placeholders, customize narrative prose in place. Same canon as the helper.

---

#### Build contract — DO

1. **Read `references/skeleton-transformer-guide.md` first.** Then read `references/build-skeleton.html` in full. Both are required before writing any HTML.
2. **Use `references/transform.py` in claude.ai. Use `cp + Edit` in Claude Code.** Either way, the skeleton file is your input — never recreated from memory.
3. **Reproduce all 7 canonical tab panels from the skeleton** — `tab-summary`, `tab-whynow`, `tab-aiportfolio`, `tab-avpanalysis`, `tab-roadmap`, `tab-assumptions`, `tab-sources`. These exist in the skeleton; you fill their content sections via `fill_section`.
4. **Preserve the `<div class="skill-attribution">` at the bottom of every tab panel.** Already in the skeleton. Do not remove it. Update the date code only if SKILL.md's `updated` differs.
5. **Add the Portfolio View Toggle when the downselect ratio is < 1.0** — this is a sanctioned addition to the sidebar. Wire `FN_DATA`, `setView`, and `body.view-prio` / `body.view-all` rules. See `references/portfolio-view-toggle.md`.
6. **Fill every `{{PLACEHOLDER}}` marker.** `Skeleton.write()` enforces this — it raises on any unfilled marker. The guide documents the canonical name for each.
7. **Use only `var(--variable-name)` for color values outside `:root {}`**. If you need a color that has no canonical variable, add it to `:root` — never write a bare hex value in a CSS rule.

#### Build contract — DO NOT

8. **DO NOT open with `<!DOCTYPE html>` typed from memory.** If you find yourself doing this, stop — you have not read the skeleton. Read it, then begin.
9. **DO NOT open a new `<style>` block from scratch** — in HTML or in a Python string. The `<style>` block is the skeleton's `<style>` block. Copy it; extend if needed; do not rewrite it.
10. **DO NOT write a second `:root {}` block.** There is one in the skeleton. Extend it by adding variables inside it if needed; do not create a second one.
11. **DO NOT add, remove, or rename a tab panel without asking the user first** — see the deviation gate below. This applies to all tabs including AVP Analysis.
12. **DO NOT write a bare hex color value in any CSS rule outside `:root {}`.** No `#888`, no `#0a3a8a`, no `#5a4000`. Every color is a `var()` reference.
13. **DO NOT omit the disclaimer band from any tab.** It is in the skeleton on all 7 tabs. Keep it everywhere.
14. **DO NOT write HTML content inside Python string literals.** Writing `html = """<!DOCTYPE html>...` or `output += "<div class=..."` in a Python script is the same anti-pattern as typing DOCTYPE from memory — it generates instead of transforms. If your Python script contains an HTML string literal that starts with `<!DOCTYPE`, stop. Delete the string. Read the skeleton file instead. The build contract DO NOT rules apply to Python code just as they apply to direct HTML authoring.
15. **DO NOT leave any `{{PLACEHOLDER}}` marker in the final output file.** The QA script hard-fails on any unfilled `{{...}}` pattern (except the two `ENGAGEMENT_DATA_START/END` wrapper comments, which are preserved as infrastructure markers). After running your transformer script, `re.findall(r'\{\{[^}]+\}\}', html)` must return an empty list (or only the engagement data markers). If it is non-empty, the build is incomplete — fill the remaining placeholders before writing output.

---

#### Deviation gate — always ask the user before deviating

A deviation is any departure from the skeleton's structure. Examples:
- Adding a tab not in the canonical 7
- Removing any canonical tab (including AVP Analysis, even though it has a documented omission rule)
- Changing the nav layout, hero layout, or sidebar structure
- Introducing a new CSS component class not present in the skeleton
- Adding a new `:root` variable beyond the canonical palette

**Before making any deviation:** stop. State the proposed change in one sentence and explain why you think it's needed. Wait for an explicit yes from the user. Do not proceed on your own judgment. There are no pre-approved exceptions — every deviation, including ones with documented rules, requires a fresh confirmation in the current session.

---

Follow `references/structural-rules.md` for nav standards, the per-UC modal architecture (10 sections including Section 7B LOE rationale), the AI Portfolio matrix block (≥1 matrix, per `references/portfolio-matrices.md`), and the cost-vs-benefit chart spec. See Phase 9 build contract above for the single source on structural rules — `structural-rules.md` is the content reference; the build contract above governs the build process. Follow `references/design.md` for all visual implementation: CSS variables, type scale, spacing, card patterns, component templates, chart containers, interaction patterns, and print fidelity.

**Chart conventions are universal — see `references/chart-conventions.md`.** Time framing (elapsed years vs elapsed months), break-even arithmetic (the `+1` shift on the JSON `breakeven` value), per-UC matrix xMin formula (`min(payback) − 2` per function — *not* `break-even − 1`, which hides the win zone), break-even annotation lines, and the heatmap 10-band bucketing. The conventions exist because their absence has produced shipping bugs.

**Standard components ship with every PoV.** The glossary panel, methodology visual, "Used for" source column, gap-explanation paragraph, tech-pill solid/dashed treatment, in-flight legend, anchor tooltips, Phase 0 cards, break-even callout, filter-sidebar prompt, and forcing-card structure are all defined in `references/structural-rules.md` — Standard components. The skill attribution footer is already in the skeleton on every tab — preserve it. Render all other standard components from the templates in `structural-rules.md` with engagement-specific values from `references/engagement-config.md`.

**Sidebar icons are engagement-specific — do not hardcode.** The collapsible left sidebar uses Lucide SVG icons for every filter button. Fixed icons (star = Prioritized, list = All Evaluated, grid = All Functions, target = All Goals) never change. For individual Function and Strategic Goal filter items, pick icons from `references/icon-palette.md` using the keyword-match table. Strategic goal items use a colored swatch (not an SVG) — colors assigned in order from the five-color palette in `references/icon-palette.md`.

**Portfolio View Toggle (Prioritized ↔ All Evaluated)** sits at the top of the function-filter sidebar — see `references/portfolio-view-toggle.md` for the full spec. Two stacked buttons swap the pool between the recommended portfolio (8–25) and the full broad pool (~50, including deprioritized). Wires four things into the build: `FN_DATA` emitted as inline JS const, `body.view-prio` / `body.view-all` CSS rules driving visibility (no inline styles), dual-pool matrix SVG with union-computed axes so bubbles don't reflow, and a single `setView(view)` JS function that composes with the function filter. Default state is `<body class="view-prio filter-ALL">`. **Suppress the toggle entirely if the downselect ratio = 1.0** (broad pool == final portfolio) — a single-state toggle is noise. The Sources tab MC paragraph must say *"10,000 trials on all {broad-pool} candidates"* — the toggle exists precisely because the rigor extends to the full pool.

**Aim and function filter chips must remain active — never commented out.** The skeleton's filter row (aim chips A1–A8 + function chips) must appear as live HTML elements in the rendered output. Do NOT wrap the filter row in `<!-- -->` HTML comments as a self-repair action. If an aim A6/A7/A8 chip references an undefined CSS class, that is a skeleton deficiency — fix by appending the missing CSS; do not suppress the filter chip. As of v2.8, A1–A8 aim CSS is fully defined in the skeleton and the `transform.py` helper enforces use of canonical class names; no CSS injection is needed.

**Canonical 7-tab default:** Summary · Why Now · AI Portfolio · AVP Analysis · Roadmap · Assumptions · Sources. Tab IDs: `tab-summary`, `tab-whynow`, `tab-aiportfolio`, `tab-avpanalysis`, `tab-roadmap`, `tab-assumptions`, `tab-sources`. The 5-tab variant drops Why Now (folded into AI Portfolio) and AVP Analysis. AVP Analysis is optional regardless of variant — present only when the user provided value-chain images at intake (Question 10). See `references/structural-rules.md` — Tab structure.

**The Roadmap tab carries two fixed sections and one five-view toggle.** Fixed sections: (1) cumulative cost-vs-benefit SVG line chart with break-even crossover annotation + Phase 0 foundation callout (excluded from portfolio totals). Five-view toggle (generated from engagement data — see content sourcing rules below): **Overview** · **Workstreams** · **Phase Gates** · **Dependencies** · **Horizons**.

**Roadmap tab — content sourcing per view:**

- **Overview** — Phase 1/2/3+ deployment cards: UC list per phase (pulled from downselect output), one-time/ongoing/annual-benefit per phase (from `financial-model.md` staggered deployment), cost breakdown table (one-time / ongoing / 5-yr cumulative / 5-yr benefit). Generated directly from Monte Carlo output and phase assignments.

- **Workstreams** — SVG swim lane across a `max(payback_month_of_last_UC) + 6` month horizon (cap 60 months). One track per: Foundation/platform (Phase 0 duration), each portfolio UC with build bar (estimated from LOE tier: Quick Win = 6 mo, Standard = 9 mo, Major Initiative = 12 mo) and lighter operate bar (payback month from go-live), Change Management (persistent full-width track), Value Realization (starts at first UC go-live). Phase background bands derived from phase assignments. Month labels on x-axis.

- **Phase Gates** — one gate card per phase boundary (Gate 1: Phase 0 → Phase 1; Gate 2: Phase 1 → Phase 2; Gate 3: Phase 2 → Phase 3+). Each card: timing badge (first UC go-live month for that phase), 4 explicit go-criteria (at least 2 must cite specific KPI thresholds derived from the UC success metrics in the engagement — e.g. "UC-01 achieving ≥X% forecast accuracy improvement"), "on no-go" consequence block. Do not use generic criteria — derive from the actual UC portfolio.

- **Dependencies** — one card per portfolio UC (not deprioritized). Four blocks per card: **Data** (source systems, data history requirements, labeling needs), **Platform** (Phase 0 or predecessor UC platform requirements), **Org readiness** (change management burden, user count, workflow changes), **Predecessor** (either "None — can start at Phase N kickoff" or a specific prerequisite UC/platform state). Predecessor field drives the phase ordering rationale.

- **Horizons** — three cards: Horizon 1 (Phase 1 UCs → Productivity → 6As: Assist + Automate), Horizon 2 (Phase 2 UCs → Differentiation → 6As: Augment + Anticipate), Horizon 3 (Phase 3+ + backlog → Disruption → 6As: Associate + Agentize). Each card carries: horizon badge, phase timeline, title, capability pattern, UC list, colored 6As pills, key measurement signals. Signal examples must match the UC domain — do not use generic signals like "efficiency improved."

**The Assumptions tab has two layers: interactive DCF parameter model + static assumption register.**

Layer 1 — four global parameter sliders with live recalculation:

| Parameter | Default | Drives |
|-----------|---------|--------|
| Discount Rate (WACC) | 9.5% | All NPV calculations |
| FTE Fully-Loaded Cost | $145k | Scales all FTE-driven benefit estimates |
| Year 1 Adoption Rate | 60% | Year 1 benefit; Years 2–5 ramp automatically to 85→90→95→100% |
| Implementation Cost Buffer | 15% | Contingency on all UC build cost estimates |

Slider changes propagate **live** to: Portfolio tab UC tile metrics (benefit, NPV, payback), table cells, and the portfolio totals footer. They do **not** update the break-even SVG chart or matrix views — those are base-case fixed and require manual recalibration when the engagement financial model is built. A caveat note on the tab states this scope explicitly.

Below the sliders: a portfolio impact summary (3 cards: portfolio NPV, annual benefit, total implementation investment — all computed, all live-updating with green/red delta vs. base case) and a per-UC impact table (6 rows, showing computed benefit, NPV, IRR, payback, investment with delta indicators).

Layer 2 — three static assumption cards (Financial Model · Technical · Delivery) containing non-parameterizable constraints (horizon, terminal value policy, model accuracy thresholds, sponsorship requirements, etc.).

**Skeleton vs. full engagement pattern:** The DCF parameter model is the skeleton placeholder. A full engagement build with active citation routing replaces Layer 1 with the [I#] inferred assumptions table + Monte Carlo confidence bands (P10/P50/P90) per `references/structural-rules.md` — Assumptions tab. The static Layer 2 cards are carried forward in both patterns.

**Default phasing is Phase 0 / 1 / 2 / 3** — four phases in the Roadmap tab Overview view, not three. Phase 0 is foundation (TBC, excluded from portfolio financial totals). Phase 1 deploys Year 0 (5-year ramp). Phase 2 deploys Year 1 (4-year ramp). Phase 3 deploys Year 2 (3-year ramp). See `references/financial-model.md` — Staggered deployment model.

**The Summary tab is hero-only.** Single-screen executive summary: title + tagline + the big-one + 2×3 supporting KPI strip + Phase 0/1/2/3 strip + 1-line context bridge. **Nothing else.** All depth (bridge waterfall, Why Now content, Strategic alignment, AI Success Patterns) lives on the **Why Now** tab in the 7-tab default or folds into **AI Portfolio** in the 5-tab variant. See `references/editorial-rules.md` — Less is more.

**Hero is options-driven, not auto-generated, and locked before render.** The skill presents 3–5 title options, 2–3 tagline options, and big-one + supporting metric options to the user at Phase 8.5 (before Phase 9 renders). The user picks. The skill does not auto-select. Each option must ground in a publicly stated client priority (10-K, earnings call, investor day, named target). **Phase 8.5 (Hero lock) gates Phase 9** — once the user picks, the skill presents a one-screen text preview and waits for an explicit "lock it" before rendering HTML. See `references/hero-lock.md`, `references/structural-rules.md` — The Hero pattern, and `references/financial-model.md` — Hero — title, tagline, and the big-one.

**The Big-One is a 7th hero metric** sized larger than the supporting strip (88–100px font), positioned above the 2×3 KPIs, picked specifically for the audience and the compelling story. Title + tagline + big-one form a coherent narrative triangle — compelling but truthful. See `references/editorial-rules.md` — Narrative cohesion.

**KPI strip order is "What it delivers" first, then "What it costs"** — value before cost. Every monetary metric must state its timing modifier (one-time / recurring / cumulative / duration).

**Citation routing.** Body-text citation references route to the correct tab on click: `[S#]` and `[B#]` switch to the Sources tab + scroll to row; `[I#]` switches to the Assumptions tab + scroll to row. See `references/structural-rules.md` — Citation routing.

**No diagonal "ILLUSTRATIVE — INDICATIVE" watermark.** The disclaimer band on every tab carries the illustrative status; the visual watermark added noise without informational value.

**AVP Analysis tab (optional)** — built only if the user provided one or more value-chain images at intake (Question 10). The image(s) are base64-embedded inline; if no image, the tab is omitted entirely. The section eyebrow inside the tab uses **"AVP TASK ANALYSIS"** — visible AVP positioning is intentional on this tab. See `references/structural-rules.md` — AVP Analysis tab.

**Slalom logo:** embed the inline SVG from `assets/slalom-logo-white-RGB.svg` directly inside `<span class="slalom-logo">`. Do not use base64, do not use external URLs, do not approximate with `<text>`.

**Editorial discipline:** Apply `references/editorial-rules.md` from the start, not as a retrofit. Visual design rules (type scale ≤9 sizes, card system ≤2 patterns, spacing on 4-base scale) are in `references/design.md`. Sentence case for headings, eyebrows reserved for category context only. The absence of these rules produces work that reads as AI-assembled even when the content is solid.

**Pre-delivery self-check — REQUIRED before Phase 10.** After writing the HTML, verify these three items explicitly before proceeding. These are the most common build failures; all three have caused delivery rework.

1. **Skill attribution footer on every tab.** Count the number of `<div class="skill-attribution">` elements in the output. It must equal the number of tab panels. Each tab panel closes with exactly one attribution div before its closing `</div>`. If ANY tab panel is missing the footer, add it before proceeding — this is a hard fail in `qa-automated-checks.py`.

2. **Portfolio View Toggle.** If ANY use cases were deprioritized (i.e., the broad pool is larger than the final portfolio), the `setView` function and `view-prio` / `view-all` CSS visibility rules MUST be present. Run the QA script with `--portfolio-toggle=required` in that case. If the downselect ratio is exactly 1.0 (no candidates were deprioritized), add the comment `<!-- portfolio-toggle-suppressed: ratio=1.0 -->` inside the sidebar div and run with `--portfolio-toggle=suppressed`. A missing toggle when the ratio is < 1.0 is a build failure, not a cosmetic issue.

3. **No hardcoded hex values in CSS rules.** Scan the `<style>` block for any hex color values (e.g., `#0a3a8a`, `#888`, `#5a4000`) that appear outside the `:root {}` variable declarations. ALL color values must use `var(--variable-name)`. The only allowed hex values in the file are the variable definitions in `:root {}` and the inline SVG Slalom logo. Any other hex value is color drift — fix it before Phase 10.

**Forcing-card tagline rule:** Every forcing-function card on the Why Now tab must carry a one-sentence plain-English tagline immediately under the title. Title without tagline reads as slogan; title + tagline + body reads as analysis. QA counts title-count == tagline-count and fails on mismatch. See `references/editorial-rules.md` — Forcing-card tagline.

**Narrative uniqueness across function panes:** Phase 1 / 2 / 3 descriptions must be **unique per function** (Phase 0 is intentionally shared boilerplate). 7 function panes × 3 deploying phases = 21 unique descriptions required, not 1 template reused 21 times. The same applies to per-UC modal narratives — function-specific tooling, anchor codes, named processes, not generic "improves productivity" stubs. QA counts uniqueness per `references/editorial-rules.md` — Narrative uniqueness and `references/qa-checklist.md` — 39 (Phase-narrative uniqueness). Boilerplate is the most reliable signal that work was templated, not written for this client.

**Anchor specificity:** Every strategic anchor must ground in named public references (specific docket, named target, dated event, named asset). See `references/anchor-specificity.md`. The specificity test: if you can swap the client name and the section still makes sense, the anchors are too generic.

### Phase 10 — QA

**Automated gate (REQUIRED — block delivery on failure):**

Run `python3 references/qa-automated-checks.py <rendered.html> --client-hq=<US|CA|UK|AU> [--portfolio-toggle=<required|suppressed>]` from the skill directory. Exit code 0 = pass (or warnings only — surface to user, OK to deliver). Exit code 1 = block delivery, return to the failing phase, fix, re-run.

Pass `--portfolio-toggle=required` when the broad pool exceeds the final portfolio (any candidates were deprioritized). Pass `--portfolio-toggle=suppressed` when the downselect ratio is 1.0. Omit the flag to get a warning-only check.

The script enforces the hard rules in `references/client-language.md` plus the v3.0 structural checks:
- DIV depth trace ends at 0 (HTML well-formed)
- All `var(--*)` CSS variable references resolved
- Substantive class names used in body have CSS rules
- No unfilled `{{PLACEHOLDER}}` template markers
- No value-badge emojis (♥ ☮ 🎓 ★ ✓ ✗) in visible content
- `bundle` word count ≤ 10 in body (convention is "Use Case")
- British spelling count ≤ 50 on US-HQ client
- Raw `[S#]`/`[I#]`/`[B#]` inline brackets ≤ 30 in body (use styled spans)
- Matrix SVG `<circle>` elements grouped in `<g data-fn=...>` wrappers (so filters reach them)
- All JS functions called via `onclick` are defined
- **(S5 — v3.0)** Skill attribution footer (`skill-attribution` class) present on every tab panel — 0 footers = hard fail
- **(I5 — v3.0)** Portfolio View Toggle (`setView` function) present when `--portfolio-toggle=required` — hard fail when missing
- **(S6 — v3.0)** Hardcoded hex values in CSS outside `:root` — hard fail when > 20 non-white instances (color drift); warn when > 8

The script is **calibrated against three internal reference builds** — `--test` flag reruns the calibration:
- Canonical golden master build: expected PASS
- Reference broken build (emojis, British spellings, untagged matrix bubbles): expected FAIL
- Reference corrected build: expected PASS

Also run the human-readable sweep in `references/qa-checklist.md` for items the script cannot mechanically check (narrative cohesion, anchor specificity, classification mix). Zero tolerance for JS syntax errors. Verify disclaimer on every tab.

### Phase 11 — Delivery

**PRECONDITION:** `qa-automated-checks.py` must exit 0. Never declare delivered while QA fails.

Write the final HTML to the output path the user confirmed at intake (Phase 1). **Also write the decisions log** (`decisions-{client}.md`) to the same directory per `references/decisions-log.md` — capture the locked hero, matrix selection, downselection overrides, design variant, and open questions. The decisions log is the resume-continuity artifact; without it, the next session re-litigates the same judgment calls.

**Design-lock check.** Before declaring delivery, walk the design-lock checklist in `references/golden-master.md` against the rendered HTML — palette, tab labels, tab IDs, hero gradient, card patterns, type scale, chart heights. Flag any drift. Drift is acceptable only when the engagement uses a non-canonical design variant (captured in `engagement-config.md` — 16) or the user explicitly authorized the deviation.

Summary to user: what was built, headline portfolio numbers, classification mix, mode used (A / B / hybrid), number of AVP features bundled, broad pool size vs. final portfolio size, downselection method (composite MC rank), number evaluated but deprioritized, matrices rendered on the AI Portfolio tab (which axis pairs and why), design variant applied (canonical or named overlay), decisions log path, any flagged gaps.

**Versioning behavior is cost-mode-dependent.** In **Optimized mode (default)**, the first complete render writes as `{client}_AI_Portfolio_v1.html`; subsequent revisions edit that same file via `Edit` rather than `Write`. Bump the version (write a new `_v2`, `_v3` file) only at the named milestones: after the user has reviewed end-to-end and given substantive feedback, and at final delivery. In **Standard mode**, bump on substantive revisions but stay in place for small edits. In **Full-fidelity mode**, bump on every render. See the **Cost mode** section below for the complete rules — including the explicit note that Optimized mode overrides the global `feedback_increment_versions_on_iteration` memory within this skill's runs.

---

## Hardcoded client-facing defaults

**These defaults apply unconditionally unless overridden at intake. Hardcoded in the skill, not in user memory — every user gets the same output.** See `references/client-language.md` for the full rules and the QA enforcement.

| Default | Value | Override at intake by |
|---|---|---|
| Language | US English | Client HQ ≠ US (intake Q8) |
| Emojis as value badges (♥ ☮ 🎓 ★ ✓ ✗) | **Forbidden** in visible content | Never — use text labels |
| "bundle" / "bundles" word | **Forbidden** in visible content | Never — convention is "Use Case" / "Use Cases" |
| Anchor codes alone (`A1`, `A2`, ..., `A8`) | **Forbidden** as standalone chip text / button labels | Never — accompany with full name (e.g., `A1 — Margin recovery` OK; `A1` alone is not) |
| Raw citation brackets (`[S5]`, `[I3]`) | **Forbidden** as inline plaintext | Render as styled spans (`<span class="s-ref">S5</span>`) |
| `HEAVY mode` label | **Forbidden** in body content | Never (per `editorial-rules.md` line 86 — internal authoring note) |
| Disclaimer text | `Illustrative analysis.` | Per `editorial-rules.md` |
| Technical terms (`Monte Carlo`, `P(NPV>0)`) | Translated to client-friendly equivalents by default | Set `audience_technical_default: true` in `engagement-config.md` — 17 |

The Phase 10 automated QA script (`references/qa-automated-checks.py`) enforces these as hard fails. The script is **calibrated** against internal reference builds — it passes the canonical golden master while failing known error categories. Run `python3 qa-automated-checks.py --test` to verify calibration.

## Localisation

**By default, all language and monetary conventions follow the nation of origin of the client company.** This includes:
- **Spelling:** Canadian English for Canadian companies (colour, centre, labour, organisation), British English for UK/AU companies, American English for U.S. companies (default — see Hardcoded defaults above)
- **Currency:** C$ for Canadian, A$ for Australian, £ for UK, € for European, US$ only when necessary to disambiguate (otherwise $)
- **Date formats:** Follow local convention
- **Regulatory/compliance references:** Reference the applicable jurisdictions (e.g., Canadian Employment Equity + U.S. EEO for a Canadian company with U.S. operations)

The user may override this. When a company operates primarily in a different market than its HQ (e.g., a Canadian company with 60%+ U.S. revenue), ask the user which convention to follow.

---

## Client-facing terminology

**Never use internal AVP terminology in the dashboard body.** The following mapping applies:

| Internal (AVP/Slalom) | Client-facing (dashboard) |
|---|---|
| Tasks | Key activities |
| Features | AI enhancements |
| Bundles / use case bundles | Use cases |
| Functions | Operations |
| Task Analysis | Activity analysis |
| Enhancement types | AI capability types |
| Business function | Operation / operational area |

AVP is mentioned in the disclaimer, the Sources tab methodology paragraph, and the AVP Analysis tab (when present) only. It never appears as a selling point in the body of the Summary / Why Now / AI Portfolio / Roadmap tabs.

---

## Two modes at a glance

| | Mode A — User-bundled | Mode B — Claude bundles |
|---|---|---|
| Input | Pre-bundled UC list | Raw AVP Enhance export files |
| Claude's bundling work | Validate mapping | Apply anchor-driven clustering to ~50 broad pool |
| Source of truth | User's bundling judgment | `bundling-logic.md` |
| Broad pool | User's list (may be <50) | ~50 candidates |
| MC + downselection | Runs on whatever the user provides; downselects if pool > target | Runs on full ~50; composite rank cuts to 8–25 |
| Fastest path | Yes | Longer intake, more iteration |
| Typical classification mix | BENCHMARK-heavy | BENCHMARK + INFERRED mix |

---

## Disclaimer posture

**HEAVY is the default.** Financial estimates are illustrative until validated against the client's actual operating model. The PoV's credibility is strengthened by this honesty, not weakened.

Downgrade to STANDARD or TIGHT only if the user confirms financial parameters have been validated by the client or by Slalom engagement work on a comparable client in the same quarter. Default to HEAVY when in doubt.

**In-flight acknowledgment + net-new proposal split is standard.** The dashboard separates what the client already has in flight (from public research and/or client-provided backlog) from what Slalom proposes net-new. This split is part of the disclaimer posture — it makes the proposition unambiguous and pre-empts the "you're claim-jumping our existing work" objection.

See `references/classification-rules.md` for the full language and when each mode applies.

---

## Cost mode

**Token economy matters.** A typical full-fidelity build of this skill consumes 100M+ tokens (mostly cache reads). The dominant driver is *full re-renders on every revision* — each new version writes a fresh 1–1.5MB HTML file and forces the next turn to re-read it in full. The Cost Mode dial controls that behavior without compromising the final artifact.

### The three modes

| Mode | Revision behavior | Version-file behavior | Typical token use | When to use |
|---|---|---|---|---|
| **Standard** | Mixed — small edits in place; substantive revisions get a new version file | Bump on substantive revisions | Moderate | Default for non-Slalom-internal users who want some traceability but not full history |
| **Optimized (default)** | **Edit in place** for all revisions until a milestone is reached | Bump **only at named milestones**: (a) first complete render, (b) after user review, (c) final delivery | ~25–35% of full-fidelity | **Default for Slalom internal use.** No quality cost — the final artifact is identical. |
| **Full-fidelity** | New version file on every revision | Bump on every render | 100% baseline | High-stakes client-facing runs where the user wants every iteration preserved as a snapshot |

The mode is picked at intake (see `references/intake-checklist.md` Question 12) and recorded in the engagement config. Default is **Optimized** unless the user specifies otherwise.

### Optimized mode — the hard rules

When **Optimized** is active:

1. **Use `Edit` for revisions, not `Write`.** Once the first complete render exists at the output path, all subsequent changes — copy edits, layout nudges, metric updates, anchor refinement, modal tweaks — go through `Edit` against that file. Do not write a new versioned file just because the user asked for a change.

2. **Bump the version number only at milestones.** Three named milestones trigger a new versioned file:
   - **v1 (or vN+1) — first complete render** at the end of Phase 9.
   - **vN+1 — after user review.** When the user has reviewed v1 (or the prior milestone) end-to-end and given substantive feedback that has been incorporated, write the new version.
   - **vN+1 — final.** When the user says "we're done" / "this is final" / "send it." Optionally tag this one as `_final` in the filename.

3. **This rule explicitly overrides the global `feedback_increment_versions_on_iteration` memory** *within this skill's runs only*. That memory still applies elsewhere. The rationale: the global rule was designed for cases where preserving prior states for review matters — within this skill, the prior state is preserved at the most recent milestone and intermediate "save points" produce no incremental value to the user but multiply token cost ~3×.

4. **When in doubt, ask.** *"This looks like a small in-place edit — keeping the file as `{client}_AI_Portfolio_v{N}.html`. Want me to snapshot a new version instead?"* The user can always escalate to a snapshot; the default is to not.

### Full-fidelity mode

Use `Write` for every revision, bump the version on every render. This mirrors the pre-v2.2 behavior of the skill. Pick this when the user has explicitly said they want a full audit trail of iterations preserved on disk.

### Optional cost levers (opt-in, not defaults)

These additional optimizations are documented for awareness. The user can opt in at intake; the skill will not apply them silently.

1. **Multi-session workflow.** Split the build into three short sessions instead of one long one: Session 1 = intake + Phase 2 research + first complete render; Session 2 = revisions + reviews; Session 3 = QA + final polish. Each session starts with a small context, collapsing the per-turn cache-read line. Trade-off: requires the user to manually carry the engagement config + the latest HTML into each new session.

2. **Externalize heavy assets.** Save heatmap PNGs, value-chain images, and other large embedded assets as separate files referenced by relative path rather than base64-embedded inline. The dashboard still renders standalone when opened from its containing folder. Trade-off: the HTML is no longer a single portable file. Use only when iteration cost matters more than portability.

3. **Haiku for mechanical QA.** Route the `references/qa-checklist.md` sweep (div balance, banned-words scan, citation coverage, panel placement) to claude-haiku via Agent invocation instead of running it in the main Opus session. Mechanical pattern checks don't need Opus. Trade-off: requires a separate Agent invocation; the substantive QA judgments (narrative cohesion, anchor specificity, classification mix) should still run on Opus.

When any of these is in effect, note it in the Assumptions tab's model methodology section so the artifact records how it was built.

---

## Version history

- **v3.4** — Filter-aware aggregation. v3.3 added cross-tab card hide/show filtering but the numbers (hero KPIs, AI Portfolio totals, Roadmap break-even chart) stayed frozen at unfiltered values. User feedback: "left panel filter is not working consistently; it should change numbers on Summary, AI Portfolio, Roadmap, and filter the heatmap on AVP Analysis." **Implementation:** new JS functions added to skeleton — `_filteredUCs()` (returns UCs matching current `_view`/`_fn`/`_goal` filter state), `_computeFilteredRoadmap()` (recomputes cumulative benefit + cost arrays from filtered UCs using phase-based ramp + meta realization/tax — defaults: P_N UC deploys Y_N at 50%, 100% Y_N+1+; cost amortized 40%/60% across phase-1+phase years then 20%/yr ongoing), `_recomputeAggregates()` (updates hero KPI strip, AP-summary stat strip, filter-status indicator, and re-renders Roadmap chart with filtered data). `_applyFilters()` now calls `_recomputeAggregates()` at end. **Phase 9 build contract addition:** include canonical IDs on hero/AP value elements: `#hero-bigone-val`, `#hero-kpi-r1-c1-val`..`#hero-kpi-r2-c3-val`, `#ap-stat-prio-count`, `#ap-stat-annual-benefit`, `#ap-stat-npv`, and `#filter-status` (badge container). Documented with example HTML in the guide. **Graceful degradation** — missing IDs simply skip the recompute for that element, no errors. CSS added: `.filter-status-badge` (amber pill visible only when filter is active).

- **v3.3** — Cross-tab sidebar filtering. v3.2 Dollar Tree concurrent runs confirmed math convergence (claude.ai $353M annual / $612M NPV vs Claude Code $328M / $662M — variance under 20% on identical inputs, both at 65% realization). New requirement: sidebar filters (View / Function / Strategic Goal) should apply across every tab, not just AI Portfolio. **Implementation:** `_applyFilters()` extended to iterate 8 cross-tab card selectors (`.anchor-card`, `.mkttrend-card`, `.competitor-card`, `.forcing-card`, `.inflight-card`, `.avp-gallery-item`, `.phase-card`, `.src-card`) plus the existing `.uc-item`. Cards carrying `data-fn` and/or `data-goal` attributes participate; cards without either are treated as universal (always visible). Phase 9 build contract updated: when filling section content for Why Now / AVP / Roadmap / Sources tabs, each card should carry `data-fn` (function name) and/or `data-goal` (strategic anchor name) where applicable. The skeleton-transformer-guide.md now documents the participating card types and example HTML.

- __HIST_**v3.4** —__ math convergence + filename convention. Concurrent v3.1 Dollar Tree runs revealed unacceptable variance: same engagement inputs produced Σ portfolio NPV of $192M (claude.ai) vs $517M (Claude Code) — 169% difference. Per-UC NPV/benefit ratio was 1.0× in claude.ai (NPV compressed, looked like 1-year benefit) vs 1.85× in Claude Code (correct 5-yr DCF). Avg per-UC payback was 20mo vs 3.7mo (5× difference; Claude Code computed `invest/benefit*12` with no realization haircut). IRR hit 500% in Claude Code (artificial cap). UC ID format diverged: UC-001 (claude.ai 3-digit) vs UC-01 (Claude Code 2-digit). **Fixes shipped in v3.2:** (1) **Per-UC math validation** added to `set_engagement_data()` — validates NPV/benefit ratio ∈ [1.2, 2.6]×, payback ∈ [3, 60] months, IRR ∈ [0, 250]%, invest ≥ $0.2M, benefit/revenue ≤ 1%. Build fails fast on methodology drift. (2) **UC ID format pinned** to canonical `UC-NN` (two-digit). `UC-001`, `UC-1`, `UC-XYZ` all rejected. (3) **Filename convention enforced** — `Skeleton.write()` requires `YYYYMMDD - Slalom AI PoV - <Client> - DRAFT v<#>.html`. Refuses on mismatch. (4) **Versioning safety** — `write()` refuses to overwrite existing files. New `Skeleton.next_output_path(client_name, output_dir, today_iso=None)` static method scans the directory for prior versions and returns the next available v<#> path. (5) **`meta` block in engagement data** — optional fields: `client`, `revenue_M`, `big_one_type` (5yr_npv | annual_benefit | payback), `realization`, `hurdle_rate`, `tax_rate`, `wacc`, `horizon_years`. `meta.big_one_type` validated; `meta.revenue_M` feeds the benefit-to-revenue UC sanity check. Pinning these explicitly per engagement is what eliminates the cross-environment variance — without `meta`, each model still picks its own realization/hurdle/tax from the engagement-config ranges. **Net effect:** the v3.1 cross-environment variance scenarios all now fail validation. To deliver, both environments must converge on per-UC math that lands inside the sanity bounds. Self-test extended from 5 negative tests to 9.

- **v3.1** — Five-issue thoroughness pass against v3.0 Dollar Tree concurrent runs (claude.ai + Claude Code). (1) **CLIENT_NAME placeholder collision** — narrative customization via post-write `html.replace('Gap to {{CLIENT_NAME}}:', ...)` silently failed because `fill_inline('CLIENT_NAME', ...)` runs first and substitutes `{{CLIENT_NAME}}` everywhere. Fix: added 7 new section markers (`ANCHOR_CARDS`, `MARKET_TRENDS`, `COMPETITORS`, `FORCING_FUNCTIONS`, `AVP_PROCESS_STRIP`, `AVP_VALUE_CHAIN`, `SOURCES`) wrapping the narrative content blocks Claude needs to customize. Now `fill_section` (which runs BEFORE `fill_inline`) replaces the entire narrative block with engagement-specific HTML. All 7 added to `REQUIRED_SECTIONS` in transform.py. (2) **Two CSS classes undefined** (`skill-attribution`, `roadmap-view`) — added explicit CSS rules in the skeleton's `<style>` block. (3a) **DIV unbalanced (depth 1 at end)** — root cause: v3.0's skill-attribution injection script for `tab-sources` placed the div outside the tab structure, creating an extra `<div id="uc-btooltip">` opening without a matching close. Fixed: moved attribution inside the tab-sources panel; removed duplicate uc-btooltip opening. (3b) **49 hardcoded hex values in CSS** — added 10 new tint variables to `:root` (`--tint-blue-bg`, `--tint-blue-soft`, `--tint-blue-border`, `--tint-amber-bg`, `--tint-amber-text`, `--tint-green-bg`, `--tint-green-text`, `--surface-3`, `--surface-4`, `--bubble-deprio`) plus restored the full canonical palette (`--coral`, `--teal`, `--purple`, `--teal-deep`, `--dark-blue`, `--hero-end`, `--surface-2`, `--rule`, `--amber`, `--amber-bg`, `--pos`, `--a1`–`--a8`, `--ph1`–`--ph3`) that v16 was missing. Replaced 214 hardcoded hex values with `var()` references. Remaining hardcoded hex: 2 (well under the 8 warn threshold). (4) **Roadmap break-even SVG chart hardcoded with Acme coordinates** — replaced 73 lines of hardcoded SVG (phase bands, gridlines, axes, polylines, data dots, break-even annotation) with a single empty `<svg id="roadmap-break-even-chart">` element + a new `_renderRoadmapChart()` JS function that reads `data.roadmap = {benefit, cost, yScaleMax, yScaleMin, yTicks, yearLabels, phaseBands, breakEven}` from the engagement-data JSON block and computes coordinates via `yScale(v) = 20 + (yMax−v)/yRange × 220`. Chart now scales to any portfolio size (Acme $65M, Dollar Tree $270M, etc.) without coordinate recomputation. (5) **Hero marker leak in Claude Code `cp + Edit` path** — added `Skeleton.strip_leaked_markers(file_path)` static method that strips orphan `<!-- {{NAME_START/END}} -->` comments from outputs built via the `cp + Edit` workflow. Idempotent; only touches whitespace-flanked marker comments. Documented as the standard post-edit cleanup step in SKILL.md Phase 9.

- **v3.0** — Skeleton replaced with the v16 design (chevron phase strip, icon-rail sidebar, slider Assumptions tab, matrix lens selector, sortable UC table, IRR vs payback matrix, source filter). v16 was the visual reference built in `claude-workspace/avp-pov-template-preview/` earlier on 2026-05-27 but never made it into the skill until v3.0. **Architecture change:** the skeleton is now data-driven — UC tiles, UC table rows, matrix bubbles, and Assumptions table rows are all rendered by JavaScript at `DOMContentLoaded` from a single `<script id="portfolio-data">` JSON block. UC count is flexible (was hardcoded to 6 in v16 source); matrix bubble positions live in `ucData[id].matrices[viewKey] = {x, y, size}` rather than inline CSS. **`transform.py` strengthened:** required-section enforcement (HERO must be filled via `fill_section`, not str_replace bypass); `set_engagement_data()` must be called explicitly; `fill_section` rejects empty content and rejects content containing its own START/END markers (catches the v2.8 marker leak-back bug); `write()` refuses on filter-chip suppression (`<!--<button class="filter-btn"`) and portfolio-toggle suppression (`<!-- portfolio-toggle-suppressed`) — the v2.7/v2.8 self-repair failure mode is now structurally rejected. **Generation guard tightened:** v3.0 expects output ratio ~1.0× skeleton (was 2.2× in v2.8) because UC content renders from data, not HTML. **Skeleton size:** 1,566 → 2,305 lines (richer template; net growth despite removing 671 lines of hardcoded UC HTML); 9 placeholders (`PAGE_TITLE`, `NAV_TITLE`, `CLIENT_NAME` ×19, `ENGAGEMENT_DOMAIN`, `ENGAGEMENT_DATA_JSON`, `HERO_START`/`HERO_END`). Acme/Manufacturing sample content remains inline in narrative areas as design-by-example — customize per engagement via Edit tool / str_replace.

- **v2.8** — Structural refactor of the build-process layer. Dollar Tree post-mortem revealed that the skeleton documented itself using the same `{{}}` syntax it was templating — a quine that broke its own regex matching. Claude.ai builds repeatedly grabbed the example `{{HERO_START}}` in the instruction preamble before the real one in the body, then generated HTML in Python strings instead of filling sections. **Deletion-first refactor:** (1) **extracted** the 141-line instruction comment from `build-skeleton.html` into a new sibling `references/skeleton-transformer-guide.md`; the skeleton is now pure HTML with each `{{MARKER}}` appearing exactly once; (2) **shipped** `references/transform.py` — `Skeleton` class with `set_engagement_data` / `fill_section` / `fill_inline` / `write` methods; `write()` refuses on unfilled markers, refuses on typo'd marker names, and refuses on > 2.2× skeleton line count (generation-vs-transformation canary); (3) **added** S7 line-count canary to `qa-automated-checks.py`; (4) **deleted** `canonical-styles.css` (310 lines) and `canonical-scripts.js` (437 lines) — duplicates of the skeleton's `<style>` and `<script>`, never kept in sync, made redundant by `transform.py`; (5) **deleted** the v2.7 CSS alias bulge (~80 lines: `.bridge-total`, `.ph-0-card`, `.forcing-cards`, `.aim-section`, `.pattern-cards`, `.avp-module-card`, `.inflight-card-title`, `.benefit-buckets`, `.profile-table` family, etc.) — aliases that papered over class-name drift now caught by the QA undefined-class check (S2); (6) **deleted** the inline Python transformer code block (~75 lines) from SKILL.md Phase 9; (7) **rewrote** SKILL.md Phase 9 build contract to direct Claude at the guide + helper, with the failure mode named directly. Net delta: skeleton down 215 lines (1,781 → 1,566), references directory down 2 files (`canonical-styles.css`, `canonical-scripts.js`), SKILL.md Phase 9 down ~75 lines. v2.7 backward-compat strips in QA S4 are retained one release as a safety net; scheduled for removal in v2.9.

- **v2.7** — Live-build QA pass on Dollar Tree engagement. Root causes: (1) `four-winning-patterns.md` explicitly cited BCG by name — contradicted `client-language.md` zero-competitor rule; `structural-rules.md` and `qa-checklist.md` had same issue — all three fixed to "leading consulting research"; (2) skeleton CSS capped at `.aim-a1`–`.aim-a5` while engagements can use up to 8 anchors — `.aim-a6/.aim-a7/.aim-a8` added to skeleton using recycled palette vars, plus `.aim-card.aim-a1`–`.aim-a8` left-border variants; (3) skeleton missing 100+ component CSS aliases (`.bridge-total`, `.ph-0-card`, `.forcing-cards`, `.aim-section`, `.pattern-cards`, `.avp-module-card`, `.inflight-card-title`, `.loe-badge`, etc.) — all added to skeleton, eliminating CSS injection on every build; (4) QA S4 check fired false-positives on `{{}}` examples inside skeleton instruction comment — fixed with `re.sub(r'<!--.*?-->', '', html)` strip before check; (5) skeleton instruction comment updated v2.5→v2.7 and expanded with CSS class quick-reference; (6) new rule: aim + function filter chips must remain active — never HTML-commented out as a self-repair action.

- **v2.6** — QA/QC hardening pass: (1) placeholder count corrected to 276 (added `{{MATRIX_DISCLAIMER_TEXT}}`); (2) transformer code block de-duped — single `import re`, single `engagement_data_script`, correct regex matching actual skeleton marker; (3) Risks tab removed from intake-checklist (dropped from canonical in v2.4, still appeared as mandatory in all three intake lists); (4) transformer code hero-timing contradiction fixed ("during Phase 9" → "at Phase 8.5"); (5) golden-master.md CSS variable count corrected from 13 to 26; (6) qa-checklist.md `panel_ids` corrected from `'phasing'` to `'roadmap'`; (7) qa-automated-checks.py hardcoded user paths replaced with `pathlib.Path`-relative paths; (8) emoji badge examples in engagement-config.md and intake-checklist.md now carry explicit "QA hard-fail" warning; (9) — symbol swept from all 23 affected files (202 occurrences); (10) British spellings corrected across all reference files (prose text); (11) `colour`/`colours` field names coordinated-renamed to `color`/`colors` across 5 files; (12) golden-master.md design-lock checklist updated to reference all 26 canonical CSS variables.

- **v2.5** — Hardening pass after a multi-iteration build shipped repeated broken versions before adopting a skeleton-driven build. Root causes: (1) references were advisory not enforced; (2) user-memory defaults (US English, no emojis, etc.) didn't transfer between users; (3) the skill had no automated gate to catch unstyled classes, undefined CSS variables, emoji visual badges, raw `[S#]` inline brackets, or untagged matrix bubbles; (4) **the build script reinvented CSS and JS from scratch every time** instead of inheriting from the canonical golden master. **Five new files + SKILL.md edits:**
  - `references/client-language.md` — single source of truth for client-facing vocabulary rules (hardcoded defaults, hard fails, translation table). Replaces user-memory-dependent enforcement.
  - `references/qa-automated-checks.py` — executable Phase 10 gate. **Calibrated** against internal reference builds — canonical golden master (PASS), reference broken build (FAIL), reference corrected build (PASS). Run `python3 qa-automated-checks.py --test` to verify.
  - `references/build-skeleton.html` — canonical structural golden master. **READ THIS FIRST in Phase 9** before writing any HTML.
  - `references/canonical-styles.css` — canonical `<style>` block extracted from the skeleton. Emit verbatim into output `<style>` tag, then append client-specific additions only. Prevents the failure mode of inventing a CSS palette from scratch.
  - `references/canonical-scripts.js` — canonical inline `<script>` content extracted from the skeleton. Same emit-verbatim pattern.
  - **Phase 10 + Phase 11 SKILL.md edits** — QA script must exit 0 before delivery. **Hardcoded defaults table** added to SKILL.md (US English, no emojis, no "bundle" word, no standalone anchor codes in chips, no raw `[S#]` inline, no `HEAVY mode` in body). These now apply per-skill regardless of user memory.

- **v2.4** — Coordinated upgrades targeting consistency and iteration cost:
  - **Risks tab introduced (later reverted).** v2.4 promoted Risks to the canonical 8th tab. Subsequently dropped from canonical entirely (~2026-05-27) — Risks is no longer part of the 7-tab default or 5-tab variant. Decisions about risk exposure live in the per-UC modal and Assumptions tab, not a standalone audience-facing tab.
  - **Phase 8.5 — Hero lock.** A gated text preview of title + tagline + big-one + 2×3 KPI strip before Phase 9 renders. Cuts in-chat iteration cost on the most-churned hero elements. See `references/hero-lock.md`.
  - **Decisions log companion.** Every build writes a `decisions-{client}.md` capturing hero lock, matrix selection, downselection overrides, design variant, open questions. Resume-continuity artifact. See `references/decisions-log.md`.
  - **Design variant registry.** Intake Q22 adds canonical (default) / Multifile / Extended / custom overlay. Engagement config — 16 captures the choice. See `references/design-variants/multifile.md` and `references/design-variants/extended.md`.
  - **Golden master pinned to canonical reference build.** Working visual canon for design-lock checks until a purpose-built canonical render exists. Tab IDs now canonical (`tab-aiportfolio` / `tab-avpanalysis`) as of v15. See `references/golden-master.md`.

- **v2.3** — Industry composite becomes a required intake field (no silent fallback to industrial defaults). 8 named sector profiles added in `engagement-config.md` — 2a: financial services (banking + insurance), SaaS/tech, retail, hospitality, telco, industrial mid-cap, energy/utilities. Healthcare providers, government, and cooperatives accommodated via the — 13 financial-structure override layered on top of the sector profile. Skill is now industry-agnostic by design at the intake gate, not just by convention.

- **v2.2** — Cost Mode dial added (`Standard` / `Optimized` [default] / `Full-fidelity`). Optimized mode enforces edit-in-place revisions and milestone-only version bumps without compromising output quality — final HTML artifact is identical to full-fidelity at ~25–35% of the token cost. Optional opt-in levers documented: multi-session workflow, externalized assets, Haiku for mechanical QA.

- **v2.1** — Non-standard financial structure support (nonprofits / government / cooperatives) via — 13 override; per-UC formula transparency with sourced variables; I# derivation chains; benefit class label overrides for sector-specific framing (e.g., "Access & capacity utilization" for nonprofit health systems); non-financial value weighting in composite ranking; in-flight Mode C (include in analysis vs. acknowledge as context); bubble chart click-to-filter interaction.

- **v2.0** — Two-stage portfolio (broad pool ~50 → composite-rank downselect to 8–25); 10K-trial Monte Carlo on the full broad pool; Phase 6.5 audience-driven matrix selection; deprioritized candidates rendered as a validated backlog.

---

## Files in this skill

- `SKILL.md` (this file)
- `assets/slalom-logo-white-RGB.svg` — the canonical Slalom logo, white-fill for dark backgrounds. Embed inline; do not approximate.
- `references/client-language.md` — **v3.0** — single source of truth for client-facing vocabulary: hardcoded defaults, hard fails enforced at Phase 10 QA, translation table for British→US English + Slalom-internal→client-facing terms
- `references/qa-automated-checks.py` — **v3.0** — Phase 10 executable QA gate. Run `python3 qa-automated-checks.py <rendered.html> --client-hq=US` to enforce client-language.md hard fails. Calibrated against internal reference builds. Use `--test` flag to reverify calibration.
- `references/build-skeleton.html` — **v3.0** — v16-based data-driven HTML template (2,305 lines). UC tiles, UC table rows, matrix bubbles, and Assumptions table rows all render from `<script id="portfolio-data">` JSON via JS at `DOMContentLoaded`. UC count is flexible. Inline placeholders: `{{PAGE_TITLE}}`, `{{NAV_TITLE}}`, `{{CLIENT_NAME}}` (19 sites), `{{ENGAGEMENT_DOMAIN}}`, `{{ENGAGEMENT_DATA_JSON}}`. Section markers: `{{HERO_START}}` / `{{HERO_END}}`. Narrative content (anchor cards, market trends, value chain steps, source citations) ships with Acme/Manufacturing sample inline as design reference — customize per engagement via Edit tool or post-write `html.replace`. Filled via `transform.py` (claude.ai) or `cp + Edit` (Claude Code). Carries: 7 canonical tab panels (Summary · Why Now · AI Portfolio · AVP Analysis · Roadmap · Assumptions · Sources), chevron phase strip, icon-rail sidebar, slider Assumptions tab, matrix lens selector (4 views: benefit-loe, npv-payback, strategic, irr-payback), sortable UC table, source filter, ~150 canonical CSS classes, ~30 JS functions including v3.0 data-driven renderers (`_renderUCTiles`, `_renderUCTableRows`, `_renderAssumpTable`, `_renderMatrixBubbles`).
- `references/skeleton-transformer-guide.md` — **v3.4** — companion read-first guide. Documents the engagement-data JSON shape (including the v3.2 `meta` block + per-UC math bounds), all section markers (`HERO` + 7 narrative sections required), every inline placeholder, the full CSS class canon (~150 classes), the JS function inventory (~30 functions), the v3.2 filename convention, and the per-UC math validation reference table. Read end-to-end before Phase 9.
- `references/transform.py` — **v3.4** — Python helper exposing the `Skeleton` class. Methods: `fill_section`, `fill_inline`, `set_engagement_data`, `write`, `strip_leaked_markers`, `next_output_path`. v3.2 contract: refuses if `{{PLACEHOLDER}}` unfilled · required sections (HERO + 7 narrative) not filled via `fill_section` · `set_engagement_data` not called · filter chips HTML-commented · portfolio toggle suppressed · output > 1.8× skeleton · content contains own START/END markers (leak-back) · empty section content · per-UC math out of bounds (NPV/benefit ∉ [1.2, 2.6]×, payback ∉ [3, 60] mo, IRR ∉ [0, 250]%, invest < $0.2M, benefit > 1% revenue) · UC ID format not `UC-NN` · output filename not `YYYYMMDD - Slalom AI PoV - <Client> - DRAFT v<#>.html` · output file already exists. Run `python3 transform.py` for self-test (9 negative tests must all PASS).
- `references/primary-source-research.md` — Phase 2 protocol (research, anchor framework, acceleration play discovery, public-language hygiene, freshness check)
- `references/anchor-specificity.md` — grounding anchors in named public references; specificity test
- `references/bundling-logic.md` — research-driven bundling (anchor-led, optional AVP score), in-flight vs. net-new separation, cuts panel, strategic-fit tier vocabulary
- `references/intake-checklist.md` — conversational intake script
- `references/classification-rules.md` — CLIENT_DATA / BENCHMARK / INFERRED rules + disclaimer scaling
- `references/benefit-classification.md` — 5-class benefit taxonomy and 3-bucket executive roll-up; CFO-defensibility patterns
- `references/financial-model.md` — Financial metric selection + NPV / payback / ramp formulas + cost narrative + cost-vs-benefit chart + 4-phase default (Phase 0/1/2/3)
- `references/monte-carlo.md` — 10,000-trial probabilistic sensitivity methodology + display patterns + multi-industry calibration
- `references/portfolio-matrices.md` — Phase 6.5 matrix selection: catalogue of axis pairs (Annual Benefit × Relative LOE, NPV × Payback, Cost Savings × Break-Even, Benefit × Break-Even, Strategic Anchor × Annual Benefit, EBITDA × Time-to-Value, P(NPV>0) × P50 NPV, Phase × Cumulative Investment, **IRR × Payback Period** [bubble size = implementation investment; add hurdle-rate dashed line when client has a stated rate; skip if modeled horizon <3 yr for most candidates]), audience → matrix shortlist mapping, relative LOE percentile computation, classification overlay, deprioritized treatment, natural-axis convention with per-matrix labeled win quadrant, rendering rules
- `references/four-winning-patterns.md` — Slalom / BCG intellectual spine
- `references/design.md` — **visual design system + accessibility**: brand palette (CSS variables), type scale, spacing scale, card system, chrome rules, nav bar spec, hero visual spec, disclaimer band, portfolio bridge visual, chart containers, CSS tooltip component, modal sizing, tech-pill treatment, in-flight visual treatment, anchor tooltips, citation highlight animation, standard component HTML/CSS templates, bubble chart interaction, dynamic chart redraw, print/PDF fidelity, **WCAG 2.1 AA accessibility** (colour contrast, semantic HTML, keyboard navigation, focus management, ARIA patterns, chart accessibility, reduced motion), visual anti-patterns
- `references/structural-rules.md` — **information architecture**: fixed vs. flexible layout, canonical 7-tab structure (Summary / Why Now / AI Portfolio / AVP Analysis / Roadmap / Assumptions / Sources) plus 5-tab variant, tab-ID naming convention (`tab-roadmap` canonical; `tab-phasing` is legacy), citation routing (S/B → Sources, I → Assumptions), per-UC modal 10-section architecture, capability-graph ingestion, anchor clustering pattern, KPI strip ordering, strategic-fit tier vocabulary, standard component content requirements (cross-refs `design.md` for templates); **Roadmap tab spec**: fixed break-even chart + 5-view toggle (Overview / Workstreams / Phase Gates / Dependencies / Horizons)
- `references/editorial-rules.md` — **content discipline**: narrative cohesion, banned-vocabulary table, sentence case headings, repetition limits, **first-use spell-outs**, **forcing-card tagline rule**, **narrative uniqueness across function panes**, **no contradictory metrics**, asterisk system, disclaimer placement, repetition-bounded basis phrasings (visual specs moved to `design.md`)
- `references/chart-conventions.md` — universal chart rules: time framing (elapsed years vs elapsed months), break-even arithmetic (the `+1` shift), per-UC matrix xMin formula, break-even annotation lines, heatmap 10-band bucketing, asterisk-on-benefit-axis convention, function-color-from-CSS-var rule, anti-patterns
- `references/icon-palette.md` — sidebar icon selection: curated Lucide SVG path data for ~30 icons, keyword→icon match tables for Function and Strategic Goal filter items, fixed icons (star/list/grid/target), swatch color palette for strategic goal items, embedding format
- `references/engagement-config.md` — Layer 2 per-engagement parameters: revenue tier, industry composite (WACC, hurdle rate, EBITDA margin, etc.), Phase 0 dollar anchor, existing tech stack baseline, strategic anchors A1–A8, heatmap stops, in-flight statuses, function color palette, in-scope functions and acronym list, "Used for" source mapping, output size budget, intake template, design variant (see 16)
- `references/qa-checklist.md` — validation sweep before delivery (benefit-sum reconciliation, function color uniqueness, phase-narrative uniqueness, internal-note leakage, filesystem-path leakage, anchor-tooltip coverage, glossary presence, Phase 0 anchoring, heatmap 10-band, break-even framing consistency, regex base64 hygiene, JSON validation, Portfolio View Toggle — 50)
- `references/hero-lock.md` — Phase 8.5 gated preview spec: the five-component preview format, the lock contract, what happens on user lock / rethink / edit responses, anti-patterns (skipping the lock, partial locks, auto-locking on silence)
- `references/decisions-log.md` — companion file spec for `decisions-{client}.md`: five sections (hero lock, matrix selection, downselection overrides + portfolio view toggle, design variant, open questions), when to update, where the file lives
- `references/golden-master.md` — pinned visual canonical (build-skeleton.html, pinned 2026-05-20); 13-CSS-variable palette comparison list; canonical tab labels and IDs; design-lock checklist; known deviations not to replicate; criteria for repinning
- `references/design-variants/multifile.md` — Multifile overlay: external CSS files + Google Fonts (DM Sans/DM Mono), `data-theme="multifile"`. Apply only on explicit user request.
- `references/design-variants/extended.md` — Extended overlay: extended palette with greens and custom dark navy, system font stack, optional Strategy and Monte Carlo tabs. Apply only on explicit user request.
- `examples/` — canonical examples (build when used)
