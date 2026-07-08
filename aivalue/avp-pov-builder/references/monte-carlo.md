# Monte Carlo Sensitivity

How to run probabilistic sensitivity on portfolio financials and surface the results without overstating precision.

This replaces the legacy "50% / 75% / 100% realization" sensitivity in `financial-model.md` with a richer treatment that produces P10/P50/P90 bands and probability metrics. **Required when financial sizing is HEAVY-disclaimer (largely INFERRED).**

---

## Why run Monte Carlo on inferred inputs

The honest framing: **MC on INFERRED inputs sharpens *sensitivity*, not *precision*.** It does not make the underlying estimates more rigorous. What it does:

1. **Quantifies the variance** that's implicit in the HEAVY disclaimer language
2. **Produces probability claims** ("70% probability of clearing the target") that are more credible than point estimates
3. **Surfaces the asymmetric risks** — typically cost over-runs hurt more than benefit upside helps, which a single sensitivity scenario hides

Always carry a caveat in the output: *"Monte Carlo bands sample plausible variance around HEAVY-disclaimer base inputs — they show sensitivity, not added precision."*

---

## Default distributions

These defaults work for most portfolios. Override only with explicit reasoning.

| Variable | Distribution | Range / SD | Why |
|---|---|---|---|
| **Annual benefit per UC** | Triangular | low = 0.60×base, mode = base, high = 1.40×base | ±40% reflects the typical INFERRED range; symmetric around base |
| **Implementation cost per UC** | Triangular | low = 0.85×base, mode = base, high = 1.50×base | Asymmetric — cost over-runs are far more common than under-runs |
| **Ongoing cost per UC** | Triangular | low = 0.85×base, mode = base, high = 1.30×base | Less skew than implementation; ongoing is more predictable |
| **Ramp realization factor** | Triangular | low = 0.70, mode = 1.00, high = 1.10 | Per-UC, per-trial multiplier on the LOE ramp curve. Reflects the 30% downside risk of slow adoption |
| **Hurdle rate** | Truncated normal | mean = 10.5%, σ = 1.5pt, clipped [7%, 15%] | Reflects uncertainty in WACC + risk-premium assumption |
| **Effective tax rate** | Truncated normal | mean = 30%, σ = 2pt, clipped [25%, 35%] | Mid-market US blended; clipped to plausible range |

**Trial count: 10,000** (sufficient for stable P10/P50/P90 to 1% precision).

**Seed: fixed** (e.g., 42) for reproducibility across runs.

---

## Calculation logic

For each trial:

```
1. Sample hurdle rate, tax rate (global)
2. For each UC:
   a. Sample annual_benefit, impl, ongoing, ramp_mult
   b. Build cashflow array using the same staggered model as base case
      (Phase 1 deploys Y0; Phase 2/3 deploy Y1)
   c. Apply ramp[i] × ramp_mult to each year's benefit
   d. Compute UC NPV(pre), NPV(AT), payback
3. Aggregate: portfolio NPV, payback, annual benefit at full ramp
4. Record per-UC and portfolio results
```

After all trials, compute P10 / P50 / P90 / mean for each metric.

---

## Probability metrics to compute

For the portfolio:

- **P(annual benefit ≥ client's stated target)** — the headline credibility number. If the engagement has a stated savings/value goal, surface this.
- **P(annual benefit ≥ 75% of base)** — robust floor signal
- **P(annual benefit ≥ 125% of base)** — upside-bounded signal
- **P(after-tax NPV > 0)** — basic project-soundness test
- **P(payback ≤ 24 mo / 36 mo / 48 mo)** — three thresholds covering typical exec expectations

Per-UC: **P(NPV > 0)** is the minimum required. Anything below 80% should be visually flagged in the modal.

---

## Display patterns

### Per-UC modal

A "Monte Carlo confidence ranges" section showing three horizontal range bars:

- **Annual benefit** — base-case marker (▼) + P50 marker (●) + P10–P90 fill band
- **After-tax NPV** — same treatment
- **Payback (months)** — same treatment

Below the bars, a **probability badge** for P(NPV > 0):
- **Green** (≥ 95%) — robust
- **Amber** (80–94%) — caveat
- **Red** (< 80%) — material downside risk; modal should explain why

### Portfolio confidence section (Assumptions tab)

A standalone section, typically titled *"Portfolio confidence under variance"*, with:

1. **Methodology paragraph** — distributions used, trial count, the "sensitivity not precision" caveat
2. **Three range cards** showing P10–P90 of: annual benefit, NPV(AT), payback
3. **Probability strip** — most decision-relevant probability flagged in green/amber:
   - Probability of clearing the client's stated target (if any)
   - Probability of positive NPV
   - Probability of acceptable payback (≤ 36 mo typical)
4. **Plain-language summary** — what's the dominant risk, what's the robust floor

Example summary lines:

- *"100% probability of positive NPV across 10,000 trials. 70% probability of clearing the $100M target. Dominant risk: implementation cost over-runs (mean spend ~11% above base)."*

---

## Composite ranking for downselection

**Purpose:** After MC runs on the full broad pool (~50 candidates), produce a single composite rank score per candidate that balances financial robustness, risk profile, and strategic alignment. This rank is the primary input to Phase 7 downselection.

### Component metrics

| # | Metric | Source | Direction | Default weight | Notes |
|---|---|---|---|---|---|
| 1 | **P50 after-tax NPV** | MC output | Higher = better | 0.20 | Central-case financial value |
| 2 | **P(NPV > 0)** | MC output | Higher = better | 0.15 | Sound-investment probability. De-weight when structurally inflated (tax < 10% AND hurdle < 8%) — see `financial-model.md` — P(NPV>0) caveat |
| 3 | **P(payback ≤ 36 mo)** | MC output | Higher = better | 0.15 | Executive patience threshold |
| 4 | **P10 annual benefit** | MC output | Higher = better | 0.15 | Worst-realistic-case benefit — penalizes high variance |
| 5 | **Strategic-fit tier** | Phase 3 | HIGHEST=4, HIGH=3, MH=2, M=1 | 0.20 | Anchor proximity — keeps portfolio tied to stated priorities |
| 6 | **Non-financial value flag** | Phase 3 | Flagged=1, Not=0 | 0.00 (default) | When activated: 0.10–0.25 per `engagement-config.md` — 15. Mission, safety, compliance, equity, ESG |

### Weight adjustment rules

**When metric 6 is activated (weight > 0):** Reduce metrics 1–4 proportionally to keep total = 1.00. Metric 5 (strategic tier) stays constant — it's the anchor-alignment signal that applies equally to financial and non-financial UCs.

Example for healthcare nonprofit (nfv_weight = 0.20):

| Metric | Default | Adjusted |
|---|---|---|
| P50 NPV | 0.20 | 0.15 |
| P(NPV>0) | 0.15 | 0.10 |
| P(payback) | 0.15 | 0.12 |
| P10 benefit | 0.15 | 0.13 |
| Strategic tier | 0.20 | 0.20 (held) |
| Non-financial value | 0.00 | 0.20 |
| **Total** | **1.00** | **1.00** |

**When P(NPV>0) is structurally inflated (all candidates near 100%):** Metric 2 loses discriminative power. Reduce its weight to 0.05 and redistribute to metrics 3 and 4 (payback and P10 benefit), which still discriminate.

### Scoring

1. **Normalize each metric to [0, 1]** within the candidate pool using min-max scaling.
2. **Weight:** Defaults above. The user may adjust weights at intake or during Phase 7 review — for example, an audience that obsesses over payback might push metric #3 to 0.30 and reduce others. Document any weight change in the Assumptions tab.
3. **Composite score = weighted sum** of the normalized metrics. Range [0, 1].
4. **Rank descending.** Ties broken by P50 NPV (higher wins).

### Presentation to user

Present the ranked list as a table:

```
Rank | ID | Name | Composite | P50 NPV | P(+) | P(≤36) | P10 Benefit | Tier | NFV | Rec
1    | UC-007 | ...  | 0.91   | $12.3M  | 99%  | 94%    | $2.1M       | HIGHEST | — | ✓ IN
...
38   | UC-022 | ...  | 0.34   | $1.1M   | 72%  | 48%    | $0.2M       | MEDIUM  | — | ✗ OUT
```

The "NFV" column shows a flag icon for UCs with the non-financial value indicator. When weight > 0, annotate the table header: *"Composite score includes [X]% weight for [category label]."* The "Rec" column reflects the target range cutoff. Candidates above the line are IN; below are OUT (evaluated but deprioritized). The user adjusts the line.

Document the weights used — including any adjustments — in the Assumptions tab model methodology section.

---

## Downselection protocol (Phase 7)

### Step 1 — Present the composite-ranked list
Show all ~50 candidates ranked by composite score with the five component metrics visible. Highlight the recommended cutoff line based on the user's target range (8–25).

### Step 2 — Identify natural breaks
Look for gaps in the composite score distribution — a cluster of candidates scoring 0.75+ and then a drop to 0.50 often suggests a natural portfolio boundary. Flag these breaks for the user.

### Step 3 — User review and override
The user may:
- **Accept the recommended cut** — proceed with the top N.
- **Pull candidates up** — a lower-ranked UC that the audience cares about survives. The user provides a reason (e.g., "CFO has named this as a pain point"). Logged as a strategic override in the Assumptions tab.
- **Push candidates down** — a high-ranked UC that domain knowledge says won't land (e.g., regulatory blocker, political sensitivity). Logged with reason.
- **Adjust the target range** — "I want 20, not 15." The composite rank re-draws the line.

### Step 4 — Classify the outs
Every candidate that doesn't make the final portfolio is classified as **"Evaluated but deprioritized"** with:
- UC ID, name, function
- Composite rank score
- P50 NPV and P(NPV>0)
- **Reason for deprioritization** — either "below composite rank cutoff" or the user's specific override reason
- **Reactivation note** — a 1-line statement of what would bring this UC back (e.g., "revisit if Phase 1 data foundation unlocks the integration prerequisite")

This list feeds the "Evaluated but deprioritized" panel on the AI Portfolio tab (see `structural-rules.md`) AND the "All Evaluated" state of the Portfolio View Toggle (see `portfolio-view-toggle.md`). Persist BOTH `final_list` and `deprio` to `mc_results.json` — Phase 9 needs both pools to wire the toggle, FN_DATA dict, and dual-pool matrix SVG.

### Step 5 — Recalculate portfolio metrics
After downselection, recalculate all portfolio-level MC metrics (aggregate NPV, payback, benefit ranges, probability metrics) using only the final portfolio. The hero, KPI strip, and Assumptions tab portfolio confidence section reflect the **final portfolio**, not the broad pool.

---

## Anti-patterns

- **Reporting MC bands as if they were tight estimates.** "5-yr NPV: $52M – $79M" without the HEAVY caveat reads as more confident than it is. Always pair with the disclaimer.
- **Hiding the asymmetry.** If the base case sits at the P85 of simulated outcomes, the base is *optimistic*, not central. State this. The honest summary acknowledges that the base is biased toward upside (because the inputs themselves were optimistic).
- **Showing too many percentiles.** P10 / P50 / P90 + mean is the right granularity. P5 / P20 / P40 / P60 / P80 / P95 is research-warehouse.
- **Comparing the MC mean to the base case without context.** If the MC mean of NPV is materially below base, the headline NPV is optimistic — say so plainly rather than burying.
- **Skipping MC on the broad pool.** Running MC on only the pre-selected 15 defeats the two-stage design. The broad pool (~50) gets full MC treatment; downselection uses the composite rank to cut.
- **Treating composite rank as a black box.** The five component metrics and their weights must be visible to the user. If the user doesn't understand why UC-007 ranked above UC-012, the downselection loses credibility. Show the math.
- **Overriding without documenting.** Every user override during Phase 7 (pulling a candidate up or pushing one down) must be logged with a reason in the Assumptions tab. Undocumented overrides make the methodology inauditable.

---

## Multi-industry calibration notes

The default distributions above are calibrated for typical mid-market enterprise AI portfolios. Adjust for:

| Industry | Adjustment |
|---|---|
| **Regulated utilities** | Cost over-run skew higher (+50% → +60%) due to OT/regulatory integration cost variance |
| **Specialty pharma** | Benefit upside wider (+40% → +60%) on revenue use cases due to regulatory-approval variance |
| **Mortgage origination** | Tighter benefit ranges (±25%) when modeling against well-documented MBA benchmarks |
| **HR / talent** | Productivity-converted benefits should use wider ramp_mult range (0.5–1.0) — adoption variance dominates |

Document any adjustment in the sensitivity methodology section of the Assumptions tab.

---

## Quick cheat sheet

```
1. Build base-case financial model first (per financial-model.md) — on ALL ~50 candidates
2. Define triangular distributions per UC for benefit, impl, ongoing
3. Define normal distributions for hurdle, tax (truncated)
4. Run 10,000 trials with fixed seed on all ~50
5. Per-UC: store annual / NPV(pre) / NPV(AT) / payback / P(NPV>0) / P(payback≤36mo)
6. Portfolio (broad pool): store same metrics + cumulative cashflow
7. Compute composite rank: normalize [P50 NPV, P(NPV>0), P(payback≤36mo), P10 benefit, tier] → weighted sum → rank
8. Present ranked list to user with recommended cutoff (Phase 7)
9. User confirms / adjusts → final portfolio (8-25) + evaluated-but-deprioritized list
10. Recalculate portfolio MC metrics on final portfolio only
11. Render in modals (range bars + P(NPV>0) badge) for final portfolio
12. Render portfolio summary on Assumptions tab
13. Render "Evaluated but deprioritized" panel on AI Portfolio tab
14. Always carry the "sensitivity not precision" caveat
```
