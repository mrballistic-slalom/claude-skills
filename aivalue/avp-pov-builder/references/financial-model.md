# Financial Model

The math behind every PoV dashboard. Defaults can be overridden if the user has a specific basis (e.g., a known WACC for the prospect), but the defaults below are reasonable for prospecting work.

---

## Financial Metric Selection

**Before building the dashboard, recommend to the user which financial metrics should headline based on audience and data quality.** This decision cascades through the hero (Summary tab), KPI strip, AI Portfolio tab chart, and Roadmap tab phase cards.

### Decision framework

| Audience | Data quality | Recommended hero metric | Recommended chart Y-axis | Supporting KPIs |
|---|---|---|---|---|
| CEO / Board / Strategy | Any | Growth/scale narrative (e.g., "C$3.6B → C$5B+") or aspirational tagline | Annual operational value vs. payback | NPV, annual cost, payback, ROI |
| COO / Operations | Medium–High | Annual operational value (C$XM/yr) | Annual value vs. payback | NPV, payback, implementation cost |
| CFO / Finance committee | High | NPV or ROI ratio | NPV vs. implementation cost | IRR, payback, sensitivity range |
| CIO / CTO | Any | Scale readiness or capability narrative | Annual value vs. payback by phase | Implementation cost, ongoing cost, payback |
| Mixed / will be forwarded | Any | Growth narrative or aspirational tagline | Annual value vs. payback by phase | Both cost and value rows (6 KPIs) |

### Metric definitions

| Metric | Formula | When to use | When to avoid |
|---|---|---|---|
| **Annual operational value** | Sum of all use case annual benefits at full ramp | Default for most audiences | When benefit estimates are heavily INFERRED and audience is finance-oriented |
| **NPV (after-tax)** | Discounted 5-year cash flows × (1 - tax rate) | Finance audiences, high data quality | Consumer-facing or non-financial audiences |
| **ROI ratio** | After-tax NPV ÷ total implementation | Board summaries, quick comparisons | When the ratio feels inflated (>5:1) and audience is skeptical |
| **IRR** | Rate at which NPV = 0 | Sophisticated finance audiences comparing against hurdle rate | When the model has irregular cash flows or the audience won't understand it |
| **Payback** | Months until cumulative cash flow turns positive | Universal — everyone understands it | Never avoid; always include as a supporting metric |
| **Annual cost to run** | Ongoing ops + compute + enablement at full deployment | Budget-oriented audiences (CIO, COO) | When ongoing costs are a small fraction of implementation |
| **Revenue/profit impact** | Benefit as % of revenue or margin | Strategy audiences | When benefit estimates are too approximate to express as a percentage credibly |
| **Scale readiness** | Qualitative ("C$5B+ ready") | Growth-focused audiences, aspirational framing | Finance committees who want numbers |

### How the metric choice cascades

| Dashboard element | Impact of metric choice |
|---|---|
| **Hero** | The headline number or narrative. Can be a financial metric, a growth narrative, or an aspirational tagline. Default: aspirational/recognition framing. User may override to a financial metric. |
| **KPI strip** | Always 6 cards in 2 rows. Top row = "What it costs" (investment, ongoing, payback). Bottom row = "What it delivers" (scale readiness or primary value metric, secondary financial metric, scope). |
| **AI Portfolio tab chart** | Y-axis = primary value metric (default: annual operational value). X-axis = payback months. Colour = phase. Size = implementation cost. |
| **AI Portfolio tab table** | Always includes: annual value, NPV, payback. Sort default = primary value metric descending. |
| **Roadmap tab phase cards** | Show the primary value metric and payback per phase. |

---

## Defaults

| Parameter | Default | Notes |
|---|---|---|
| Hurdle rate | 10.5% | Typical mid-market WACC + small risk premium. Override with prospect's actual WACC + 2-4% if known. |
| Effective tax rate | 30% | Reasonable US federal + state blend post-TCJA. Override with prospect's effective tax rate from 10-K if known. |
| Time horizon | 5 years (default); 7 years when triggered. See Decision rule below. | — |
| Currency | Follows company's nation of origin | See SKILL.md — Localisation. Display as C$X.XM, A$X.XM, £X.XM, €X.XM, or $X.XM as appropriate. |

---

## Time horizon — decision rule

Default: 5-year horizon. Switch to 7-year when:

**Phase 3 implementation cost ≥ 30% of portfolio total implementation cost AND Phase 3 LOE distribution is dominated by `MAJOR_INITIATIVE` (>50% of Phase 3 UCs).**

Rationale: a 5-year horizon truncates Phase 3 function-reshape value capture (deploy Year 2 + 5-year ramp = full benefits captured at Year 7). Truncated horizons produce misleadingly negative NPVs that obscure the strategic logic of the portfolio.

When 7-year horizon is used, disclose the choice + reason on every monetary KPI (e.g., "NPV after-tax (7-yr cumulative, $M)"), in the disclaimer band's Note on scope, and in the Sources tab methodology paragraph + Assumptions tab model methodology section.

Costs continue to discount at the standard hurdle (10.5% default) through the chosen horizon.

---

## Staggered deployment model — default is four phases (Phase 0 / 1 / 2 / 3)

**Default phasing is Phase 0 / 1 / 2 / 3.** Simultaneous deployment of all use cases is not realistic, and collapsing everything into Phase 1 + Phase 2 buries the function-reshape narrative that lives in Phase 3.

| Phase | Role | Implementation timing | Benefit ramp | Ramp years within 5-year horizon |
|---|---|---|---|---|
| **Phase 0 — Foundation** | Governance, platform standardization, MLOps, responsible AI, regulatory assurance overlay | Parallel to Phase 1 | N/A — foundation work, not in financial portfolio | 0 (TBC dollars; not financially modeled) |
| **Phase 1 — Deploy Year 0** | Deployable on current stack and operating model. The highest-strategic-fit, fastest-payback portion of the net-new portfolio. | Year 0 | Years 1–5 | 5 years of ramp |
| **Phase 2 — Deploy Year 1** | Riding the new stack at scale. | Year 1 | Years 2–5 | 4 years of ramp |
| **Phase 3 — Deploy Year 2** | Deepest workflow redesign. Function reshape. Depends on Phase 1 + 2 being live. | Year 2 | Years 3–5 | 3 years of ramp |

**Phase 0** is always TBC dollar figures (see — Foundation handling) and runs parallel to Phase 1 prep — it doesn't deploy use cases of its own.

Each later phase has its implementation cost discounted by an additional year and receives correspondingly fewer years of benefit ramp within the 5-year horizon. This produces conservative, defensible NPV and payback figures.

**If the user explicitly requests a 3-phase plan** (Phase 0 + 1 + 2 only): Phase 2 absorbs Phase 3 use cases. Document this as an exception, not the default.

---

## Ramp factors (by LOE tier)

> **Note — two LOE measures, different jobs.** The categorical **LOE tier** (Quick Win / Standard Project / Major Initiative) defined and used in this document drives ramp curves and compute surcharges. The **relative LOE percentile** (0–100, computed across the broad pool) is a separate measure used for matrix-axis storytelling on the AI Portfolio tab — see `portfolio-matrices.md` — The relative LOE percentile. Don't conflate them: the tier is operational classification, the percentile is relative ranking.

These reflect typical enterprise AI adoption curves. Apply to gross benefit per year.

| LOE tier | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Quick Win | 50% | 85% | 100% | 100% | 100% |
| Standard Project | 35% | 65% | 90% | 100% | 100% |
| Major Initiative | 10% | 30% | 65% | 85% | 100% |

**Rationale:** Quick wins ride existing infrastructure → fast realization. Major initiatives require new capability buildout → slow ramp, full value in Year 5.

---

## Cost model — three layers

### Layer 1: Implementation (one-time)

Base implementation covers: solution design, development, model training, testing, deployment, and integration.

**Organisational enablement surcharge: +25% of base implementation.** This covers training, adoption support, process redesign, capability building, and user acceptance. Always applied by default.

```
impl_total = impl_base × 1.25
```

### Layer 2: Ongoing operations (annual)

Operational maintenance: team costs, monitoring, business oversight, model performance management.

### Layer 3: Compute and infrastructure (annual)

GCP/cloud inference, storage, model retraining, MLOps tooling. Applied as a surcharge by LOE tier:

| LOE tier | Annual compute surcharge |
|---|---|
| Quick Win | $0.05M/yr |
| Standard Project | $0.10M/yr |
| Major Initiative | $0.18M/yr |

### Layer 4: Ongoing organizational enablement (annual)

Continuous improvement, ongoing change management, capability maintenance: $0.03M/yr per use case.

### Total ongoing

```
ongoing_total = ongoing_ops + compute_surcharge + 0.03
```

Display in dashboard detail rows as **"Ongoing (ops + compute + enablement)"**.

---

## Cost narrative — phased framing required

A single "Total investment: $X" headline produces sticker shock. Always express the investment profile in three time horizons:

1. **One-time, phased across deployment years** — Phase 1 implementation deploys Y0; Phase 2 / 3 deploy Y1 in parallel. The Y0 ask is typically much smaller than the headline (often <10% of total).
2. **Ongoing run cost from steady-state** — annual operations + compute + enablement.
3. **Cumulative total cost over the horizon** — sum of phased one-time + ongoing × (horizon − Y0).

### Investment KPI display pattern

```
INVESTMENT PROFILE
$XM total
~$AM Year 0 + ~$BM Year 1 (one-time, phased)
+ $CM / yr ongoing run cost from Year 2
```

(Five-year cumulative figure lives in the cost-vs-benefit chart, not the KPI strip — see below.)

This reframe converts "$X commitment now" into "small Y0 pilot, larger Y1 commitment after Y0 telemetry, then steady-state run cost." A CFO can approve the small Y0 ask immediately; the larger Y1 ask is informed by real data.

### Cost-vs-benefit cumulative chart

Required on the Roadmap tab. Replaces the legacy "stacked bars by phase + cumulative line on secondary axis" pattern, which is harder to read at exec scan-pace.

**Spec:**
- Two lines on the same axis:
  - **Cumulative cost** in red (`#d63d4f`) — sums one-time + ongoing year by year
  - **Cumulative benefit** in green (`var(--pos)`) — sums annual benefit (with ramp factors) year by year
- X-axis: Years 0 through horizon
- Y-axis: Cumulative US$ M
- Both lines start at Y0 and trend up; benefit line crosses cost line at portfolio breakeven
- Tooltip on each point: "$XM at Year N"

**Three callout cards above the chart** (the executive scan):
1. **Year 0 ask** — the small upfront commitment (often Phase 1 only)
2. **Breakeven** — months to crossover (compute from cumulative cashflow)
3. **Net by Year N** — cumulative net at horizon end (the "is this worth it" answer)

The three callouts give a ~5-second answer; the chart confirms.

### Year-by-year cost computation

For each UC:
```
Y0 cost = impl × (1 if phase 1 else 0)
Y_k cost = ongoing × (1 if UC has deployed by Y_k else 0)
```

For Phase 1 UCs deployed Y0, ongoing starts Y1.
For Phase 2 / 3 UCs deployed Y1, ongoing starts Y2.

For each UC, year-by-year benefit:
```
Y_k benefit = annual_benefit × ramp[k - deploy_year - 1] × ramp_realization_factor
```

Roll up to portfolio totals; cumulative is running sum.

### Anti-patterns

- Headline "$XM total investment" without phasing — triggers sticker shock immediately
- Ongoing run cost hidden in a separate KPI / tab — makes total cost feel deceptive
- Cumulative-cost line shown on secondary axis with stacked bars — harder to read; the simpler two-line cumulative chart wins
- Showing breakeven only as "30-month payback" without a visual — abstract; the chart makes it concrete

---

## Portfolio realization factor (HEAVY-disclaimer engagements)

A multiplicative factor applied to per-UC annual benefits to dampen the headline value to a defensible expectation, without altering each UC's documented full-deployment basis.

**When to apply:**

- HEAVY-disclaimer engagements (default for cold prospects without prospect-validated financials)
- INFERRED-heavy financial models (>60% of benefit lines classified INFERRED)
- Audiences likely to scrutinize the headline number against industry benchmarks

**Default value:** 0.65 (65% realization).

**How it's applied:**

- Per-UC `annual_benefit_modeled_M` = `annual_benefit_M` × factor
- Costs (implementation, ongoing) are NOT reduced — costs are 100% as modeled (we're not optimistic about cost overruns)
- NPV, payback, MC bands all recompute from the modeled annual benefit
- Per-UC modals show BOTH `annual_benefit_M` (full deployment) AND `annual_benefit_modeled_M` (modeled value) — full-deployment basis preserved for drill-down

**Asterisk system (display convention):**

- Every benefit-derived metric in body text carries an asterisk (`*`) after the number (e.g., `$211M/yr*`, `$72M*` NPV, `41 months*` payback)
- Cost-side metrics carry NO asterisk (costs are 100% as modeled)
- One definition line per tab, near the disclaimer band, defines the asterisk:

> *"\* Modeled at 65% portfolio realization. Delivery experience shows AI portfolios capture roughly two-thirds of full-deployment value — the rest emerges during development and deployment. Per-UC basis on drill-down."*

**Methodology paragraph (Assumptions tab — model methodology section):**

> *"Full-deployment value assumes everything goes according to plan. Delivery experience shows the realistic gap is roughly one-third — driven by integration complexity, adoption pace, dependency sequencing, and scope re-discovery during development and deployment. The 65% factor isn't a hedge; it's the difference between strategy and reality."*

**When to override the default 0.65:**

- **Higher (0.70–0.75):** client has named operational AI maturity benchmarks above industry average; engagement has prospect-validated parameters on most UCs
- **Lower (0.55–0.60):** regulated industries with multi-year integration windows (utilities, payers); INFERRED-heavy models with thin benchmarks

Document the factor and its basis in `meta.portfolio_realization_factor` and `meta.realization_basis` in the financials JSON.

---

## Per-UC computation (staggered, four-phase default)

```
impl = impl_base × 1.25          # with organizational enablement surcharge
ongoing = ongoing_ops + compute + 0.03  # all ongoing layers

# Phase 1: deploy Year 0 (5-year ramp)
cf[0] = -impl
cf[i+1] = (annual_benefit × ramp[i]) - ongoing   for i in 0..4

# Phase 2: deploy Year 1 (4-year ramp)
cf[1] = -impl
cf[i+2] = (annual_benefit × ramp[i]) - ongoing   for i in 0..3

# Phase 3: deploy Year 2 (3-year ramp)
cf[2] = -impl
cf[i+3] = (annual_benefit × ramp[i]) - ongoing   for i in 0..2

npv = sum(cf[i] / (1 + hurdle)^i for i in 0..5)
npv_at = npv × (1 - tax_rate)
pb = months_to_cumulative_positive(cf)
```

For payback: walk year-by-year cumulative cash flow; when it crosses zero, interpolate within that year to a fractional month. Cap at 60 months if it never crosses positive in 5 years.

---

## Portfolio totals

Sum the UCs:
```
T.impl = sum(b.impl for b in use_cases)
T.ongoing = sum(b.ongoing for b in use_cases)
T.annual = sum(b.annual_benefit for b in use_cases)
T.npv = sum(b.npv for b in use_cases)
T.npv_at = sum(b.npv_at for b in use_cases)
```

Portfolio payback uses the *aggregated* cash flow:
```
pcf[i] = sum(b.cf[i] for b in use_cases) for i in 0..5
T.pb = months_to_cumulative_positive(pcf)
```

---

## Sensitivity — Monte Carlo (preferred)

Use the Monte Carlo methodology in `monte-carlo.md` for HEAVY-disclaimer engagements. 10,000-trial probabilistic sensitivity produces P10 / P50 / P90 ranges and probability metrics that are far more credible than three-scenario point estimates.

The legacy three-scenario approach below remains acceptable for STANDARD or TIGHT disclaimer modes where the financial parameters have been validated.

## Sensitivity — three-scenario (legacy)

Recompute NPV at three realization levels: 50% / 75% / 100% of base benefits. Costs stay at 100% (we're not optimistic about cost overruns).

```
total_bPV = sum across all UCs of (benefit × ramp[i]) discounted at hurdle
total_cPV = sum across all UCs of impl discounted + ongoing discounted

conservative_npv = 0.50 × total_bPV - total_cPV
base_npv = 0.75 × total_bPV - total_cPV
optimistic_npv = 1.00 × total_bPV - total_cPV
```

**Important:** The "base case" displayed in the dashboard is the sum of use case NPVs (which assumes 100% realization at the use case level). The 75% sensitivity scenario is shown as the "conservative-base" interpretation.

---

## Foundation handling

**Always exclude foundation cost from the portfolio financial model.** Foundation work (platform, MLOps, governance, talent) is real and required, but its scope and cost depend on prospect-specific infrastructure that can't be sized from outside.

Display in the dashboard:
- Phase 0 Foundation card with description and component breakdown
- "Scope & Cost: TBC — scoped during validation" instead of dollar figures
- **Phase 0 caveat visible in the hero section** — not just in the disclaimer. The caveat must be readable without scrolling past the hero. Example: *"Excludes Phase 0 foundation investment (AI governance, GCP platform standardisation, MLOps tooling, responsible AI framework) — scoped during validation. All figures represent use case investment only and are illustrative pending discovery."*
- Disclaimer note echoes the same

This was a hard-won lesson from earlier dashboard iterations where invented foundation numbers couldn't be defended in front of finance audiences, AND where burying the caveat in disclaimers allowed readers to take headline numbers at face value without context.

---

## Hero — title, tagline, and the big-one

The hero combines **three elements**: title, tagline, and the big-one metric. They form a coherent narrative triangle. See `structural-rules.md` — The Hero pattern.

**The skill presents options for all three at build time** — the hero is not auto-generated. The skill proposes 3–5 candidates per element with rationale, recommends one, and lets the user pick.

### The big-one — the dominant takeaway metric

A single, large, prominently sized number positioned above the supporting 2×3 KPI strip. The big-one is the number the audience should remember if they remember nothing else.

#### Recommendation logic

The skill recommends a big-one based on **audience** and **story strength**:

| Audience | Strong big-one candidates | Why |
|---|---|---|
| **CEO / Board / Strategy** | Scale narrative ("[N]M-customer precision at 1:1 scale"), aspirational growth ("[$N]B [stated metric] ramp"), or after-tax NPV | Strategic frame, not operational detail |
| **CFO / Finance committee** | After-tax 5-yr NPV ("[$N]M"), or a clean ratio ("[$N.NN] net per $1 invested") | CFO-defensible, financial proof |
| **COO / Operations** | Annual operational value ("[$N]M/yr"), or productivity translation | Recurring impact in their P&L |
| **CIO / CTO** | Use case scope + readiness ("[N] use cases · [$N]M run-rate value") | Deliverability frame |
| **CMO / CRO** | Incremental revenue ("+[$N]M net-new top line") | Growth and acquisition story |

#### Truthfulness rules (mandatory)

- **Never combine across timing without labeling.** "$294M" is fine; "$1B over 5 years" is fine; "$1B" without a horizon label is misleading.
- **Never round upward by more than 5%.** A computed $292.4M displays as $292M, not $300M.
- **Never use a pre-tax ratio when an after-tax ratio is available.** A finance audience catches it immediately.
- **Never combine cost-side savings + incremental revenue + cost avoidance into a single number** unless explicitly labeled as "total benefit" — most CFOs distinguish these.
- **Never hide an order-of-magnitude assumption.** If the number depends on a cost-of-acquisition multiplier or a productivity uplift assumption, the basis lives in the modal — but the dashboard's transparency table on the Roadmap tab discloses it.

#### Visual treatment

See `design.md` — 8 for the full hero visual spec (gradient, type sizes, KPI strip layout). Key rendering notes for the financial content:

- Sub-text below the big-one: timing modifier + qualifier (e.g., "5-year cumulative, after-tax · @ 12% hurdle") — 13px, opacity 0.85
- The big-one and the supporting 2×3 strip together form the hero's metric block

### The supporting six (the 2×3 KPI strip)

Six KPIs in two rows, "What it delivers" on top, "What it costs" on bottom — see — KPI strip below. The skill presents options for which six to include; the user picks. The big-one is always *additional* to the six, not one of them.

### Title and tagline

The skill presents 3–5 title options grounded in the client's brand language, stated priorities, and competitive context. Once title is chosen, 2–3 tagline options under it. See `structural-rules.md` — The Hero pattern for the options-driven build process and `editorial-rules.md` — Narrative cohesion for the truthfulness constraint across title + tagline + big-one.

### Legacy hero ratio (still available if user requests it)

If the user explicitly wants the hero to be a single financial ratio:

```
hero_ratio = T.npv_at / T.impl   # after-tax, not pre-tax
```

Display as `$X.XX : $1` — after-tax net dollars returned per dollar invested. Always label as after-tax. **Never display a pre-tax hero ratio.**

---

## KPI strip — 2×3 structure

Six KPIs in two labelled rows of three. **Order: "What it delivers" on top, "What it costs" on bottom — value before cost.**

Every monetary KPI carries an explicit timing modifier in its sub-text — never just a number with no timing context.

**Top row — "What it delivers":**
1. Primary value metric — context-dependent (scale readiness, annual operational value, NPV, etc.). See — Financial Metric Selection. Sub-text: timing modifier (e.g., *"at full deployment, recurring annual"* for annual value; *"5-year cumulative, after-tax"* for NPV).
2. Secondary financial metric — the next-most-relevant metric for this audience. Sub-text: timing modifier.
3. **Third KPI — selection menu** (see below).

**Third KPI (top row, "What it delivers," card 3) — selection menu:**

Default: scope (use case count + anchor count, e.g., "15 use cases · 7 strategic anchors").

Alternatives based on audience and portfolio characteristics:

- **Anchors covered + breakdown** (e.g., "6 strategic anchors · A1–A5, A7") — preferred when anchor coverage is uneven
- **MC confidence** (e.g., "100% probability of positive NPV") — preferred when MC bands are tight and the confidence is the punchline
- **ROI ratio** (e.g., "1.3× after-tax NPV per $1 invested") — preferred for CFO-leaning audiences
- **Annual benefit** (modeled, recurring annual) — only if not already the big-one (avoid duplication)

**Forbidden in this slot:** phase shape (e.g., "2 P1 · 5 P2 · 3 P3"). Phase shape duplicates the Phase strip below the KPI grid; rendering it as a KPI reads as cryptic and adds no information. The Phase strip carries the phasing story.

**Bottom row — "What it costs":**
1. Total investment (incl. organizational enablement +25%) — `T.impl`. Sub-text: *"one-time, phased across deployment years"*.
2. Annual run cost (fully deployed) — `T.ongoing`. Sub-text: *"recurring annual, ops + compute + enablement"*.
3. Portfolio payback — `T.pb`. Sub-text: *"months to cumulative cash-flow positive"*.

Row labels ("What it delivers" / "What it costs") are visible and rendered as grid-spanning headers above each row.

### Timing modifier convention (mandatory)

Every monetary KPI in the dashboard — hero, modal, callout cards, table cells — must include one of these timing modifiers either in the value itself ($XM/yr) or in the sub-text:

| Timing modifier | When to use | Display pattern |
|---|---|---|
| **One-time** | Implementation cost, Year-0 ask, capital outlay | "$XM (one-time)" or "$XM" with sub-text "one-time, phased" |
| **Recurring annual** | Run cost, annual benefit, ongoing ops | "$XM/yr" or "$XM" with sub-text "recurring annual" |
| **Cumulative** | NPV, 5-year totals, cumulative cost-vs-benefit | "$XM" with sub-text "5-year cumulative, after-tax" |
| **Duration** | Payback, breakeven, ramp years | "X months" or "X years" |

A KPI without a timing modifier is incomplete and will be flagged by QA. A CFO reading "$174M" needs to know whether that's one-time, recurring, or cumulative — never make them infer.

---

## The compounding curve test

After computing all UCs, check the matrix story:
- Quick Wins (Phase 1): should cluster at fast paybacks (≤18 months for staggered model) and small bubbles
- Scale Plays (Phase 2): longer paybacks (24–48 months for staggered model) but higher annual values

If Phase 2 use cases uniformly have lower annual values than Phase 1, the benefit estimates may be under-scoped — Phase 2 use cases should represent workflow redesign and function reshaping, which typically produces larger benefits than edge optimisation.

---

## Currency, rounding, and display

- All internal computation in floats with 2-decimal precision
- Display rounded to 1 decimal: `C$24.3M`, `€153.2M`
- Round portfolio totals to 1 decimal AFTER summing (not before, to avoid drift)
- Hero ratio: 2 decimals (when financial hero is used)
- Payback: integer months
- Percentages (ROI, sensitivity multiples): 1 decimal
- Currency symbol follows company's nation of origin (see SKILL.md — Localisation)

---

## Non-standard financial structures

The default parameters (10.5% hurdle, 30% tax) assume a for-profit mid-market corporation. When the engagement target has a different financial structure, override both and document the basis.

### Decision tree

```
Is the organization tax-exempt (501(c)(3), government, cooperative)?
  YES → Set effective_tax_rate_pct = 0%
         Set hurdle from cost of debt or regulatory return:
           - Nonprofit with investment-grade bonds: bond yield + 1-2%
           - Government: OMB A-94 rate or jurisdiction equivalent
           - Cooperative: member cost of capital or regulatory ROE
         → Activate P(NPV>0) caveat (see below)
  NO  → Use defaults or prospect's disclosed WACC + risk premium
```

### P(NPV>0) caveat — mandatory when tax < 10% AND hurdle < 8%

When the combination of low tax and low hurdle structurally inflates NPV, the MC probability of positive NPV approaches 100% for most use cases. This is mathematically correct but misleading as a credibility signal — the audience may interpret "100% probability" as certainty, when it actually reflects the financial structure, not the estimate quality.

**Caveat language (add to Assumptions tab model methodology AND Summary tab hero):**

> *"This organization's [structure type] financial structure ([X]% tax, [Y]% hurdle) produces structurally favorable NPV compared to for-profit benchmarks. Payback months and the portfolio realization factor — not NPV probability — are the appropriate credibility measures for this analysis."*

**Shift emphasis in the hero and KPI strip:**
- De-emphasize NPV probability (don't feature P(NPV>0) as a KPI card when it's 100%)
- Emphasize payback months (universally understood, structure-independent)
- Emphasize the realization factor (the honest expression of estimation uncertainty)
- The per-UC formula basis is the ultimate credibility anchor — it's where the audience decides whether to trust the numbers

### Realization factor calibration by sector

The default portfolio realization factor (0.65) is calibrated for typical mid-market enterprise AI portfolios. Adjust for sector characteristics:

| Sector | Suggested range | Rationale |
|---|---|---|
| **Technology / SaaS** | 0.70–0.80 | Faster adoption cycles, existing data infrastructure, engineering-native culture |
| **Financial services** | 0.60–0.70 | Regulatory review cycles, model validation requirements, data governance overhead |
| **Healthcare** | 0.55–0.65 | Clinical validation, EHR integration complexity, regulatory burden, change management in clinical workflows |
| **Manufacturing / industrial** | 0.60–0.70 | OT/IT convergence, brownfield integration, union/labor considerations |
| **Government / public sector** | 0.50–0.60 | Procurement cycles, multi-stakeholder approval, legacy system constraints |
| **Regulated utilities** | 0.55–0.60 | Rate case recovery constraints, multi-year integration, regulatory pre-approval |
| **Retail / consumer** | 0.65–0.75 | Customer-facing AI adopts faster; back-office AI faces standard enterprise friction |

Document the chosen factor and its rationale in `engagement-config.md` — Industry composite and in the Assumptions tab model methodology.
