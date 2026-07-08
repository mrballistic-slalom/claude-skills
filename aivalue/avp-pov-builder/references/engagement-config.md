# Engagement Config

Per-engagement parameters that the universal rules in `editorial-rules.md`, `structural-rules.md`, `qa-checklist.md`, and `chart-conventions.md` consume to render a client-specific dashboard.

**Layer split:**
- **Layer 1 — universal** (those four files): structure, conventions, validation rules. Same for every engagement.
- **Layer 2 — engagement** (this file): the specific values for the current client. Must be captured at intake (`intake-checklist.md`) before render.

When you ship a dashboard, walk through every parameter below and either fill it from intake / Phase 2 research, or accept the documented default. Don't mix engagements — every dashboard derives from a single complete engagement config.

---

## 1. Revenue tier

The archetype's revenue scales most other defaults (Phase 0 anchor, headcount, IT spend, materials cost).

| Field | Source | Default |
|---|---|---|
| `revenue_usd` | Intake Q on archetype profile, validated against 10-K if public | — (no default) |
| `revenue_label` | Display string (e.g., `$7B U.S. mid-cap diversified manufacturer`) | — |

**Phase 0 dollar anchor scales with revenue** — see — 4.

---

## 2. Industry composite

Industry composite values feed financial defaults: WACC, hurdle rate, EBITDA margin (or sector-appropriate proxy), working capital ratio, IT spend ratio, marketing spend ratio, realization factor.

**REQUIRED at intake — no silent default.** Pick an industry profile from — 2a below, or capture each field from the client's 10-K. The skill **must not** proceed past Phase 1 without these values populated. There is no fallback to "industrial mid-cap" — if the client is non-industrial and the user hasn't picked a profile, the intake stops and asks.

For non-standard organizations (nonprofits, government, cooperatives, sovereign-backed), use — 13 (Financial structure override) **in addition to** the profile — the profile sets sector economics, — 13 sets the tax / hurdle / discount-rate framing.

| Field | Source |
|---|---|
| `wacc_pct` | 10-K disclosed WACC if available, else industry profile (see 2a) |
| `hurdle_rate_pct` | Stated internal hurdle if disclosed, else WACC + 3–5% risk premium (profile-specific) |
| `ebitda_margin_pct` *(or sector proxy — see — 2a)* | Most recent 10-K, or profile composite |
| `effective_tax_rate_pct` | 10-K (or — 13 for non-standard structures) |
| `working_capital_usd` *(or sector proxy)* | 10-K |
| `it_spend_ratio_pct` | 10-K if disclosed, else industry profile |
| `marketing_spend_ratio_pct` | 10-K if disclosed, else industry profile |
| `headcount` | Most recent 10-K |
| `monte_carlo_horizon_yrs` | Engagement preference (5 typical; 7 for regulated / long deployment cycles) |
| `portfolio_realization_factor` | Industry profile — 2a; tightens with client-validated parameters |

These appear directly in the **Glossary panel** (financial terms column), the **Assumptions tab** I-rows, and the **gap-explanation paragraph**. Update the glossary panel content to use the engagement's actual captured values.

Document the chosen profile (and any per-field overrides from the client's 10-K) in the Assumptions tab basis column. The dashboard should never display a composite the user didn't explicitly select.

---

## 2a. Industry profiles

Pick one at intake. Numbers are indicative composites — replace with the specific client's disclosed values from their 10-K when available. Sources for each composite: public 10-K disclosures from the largest 5–10 companies in the sector, mean of disclosed ranges; realization factors aligned to `financial-model.md` — Portfolio realization factor sector calibration.

| Profile | WACC | Hurdle | EBITDA margin (or proxy) | Tax | IT spend %rev | Marketing %rev | Working capital %rev | Realisation factor | Notes |
|---|---|---|---|---|---|---|---|---|---|
| **Financial services — Banking** | 8.5–9.5% | 12–14% | *Proxy:* efficiency ratio 55–65% | 22–25% | 7–10% | 2–3% | *Proxy:* loan-to-deposit ratio | 0.60–0.70 | EBITDA not meaningful for depositories. Frame AI benefits as **efficiency-ratio improvement (points)** or **non-interest expense reduction**. Hurdle reflects regulatory capital cost premium. |
| **Financial services — Insurance** | 7.5–8.5% | 11–13% | *Proxy:* combined ratio 95–102% (P&C) / operating margin 8–12% (Life) | 22% | 4–6% | 3–5% | *Proxy:* reserves & float, not standard WC | 0.60–0.70 | Frame AI benefits as **combined-ratio improvement** (P&C) or **expense-ratio reduction** (Life). Regulatory review cycles slow realization. |
| **SaaS / Tech (mature)** | 10–12% | 14–16% | 20–35% | 22% | 15–25% *(revenue IS IT spend)* | 25–40% *(growth-stage higher)* | 5–10% | 0.70–0.80 | Higher WACC reflects equity-financed structure. IT/marketing ratios are not directly comparable to other sectors — treat as upper-bound expense pools, not "addressable" via AI in the usual sense. Faster realization: engineering-native culture, modern data stack. |
| **Retail (mass / specialty)** | 7–8% | 10–12% | 5–10% | 25% | 2–3% | 4–6% | 15–25% *(inventory-heavy)* | 0.65–0.75 | Customer-facing AI realises fast; back-office AI realises at sector average. Watch for promo-rebate offsets in revenue lift use cases. |
| **Hospitality / consumer services** | 8–9% | 11–13% | 15–25% | 22% | 3–4% | 5–7% | 5–10% | 0.65–0.75 | Property-level operating leverage matters; hero metrics often per-property or per-stay rather than enterprise total. |
| **Telco** | 6.5–7.5% | 9–11% | 30–40% | 22% | 5–7% *(plus heavy capex)* | 3–5% | 10–15% | 0.65–0.75 | Capex-heavy; AI investment competes with network spend. Frame realization against multi-year network refresh cadence. |
| **Industrial / manufacturing mid-cap** | 9.0–9.5% | 12–14% | 8–12% | 22–25% | 3.5–4.5% | 2.5–3.5% | 18–22% | 0.60–0.70 | The historical default. OT/IT convergence and brownfield integration drag realization. |
| **Energy / utilities (regulated)** | 5–7% | 7–9% | 25–35% *(vertically integrated)* | 22% | 2–3% | 1–2% | 5–10% | 0.55–0.60 | Rate-case recovery constraints; multi-year integration windows; pre-approval cycles. Hurdle rate reflects regulated cost of capital. |

**Healthcare providers (hospital systems, IDNs):** most are non-profit. Use — 13 (Financial structure override) for the tax/hurdle frame — typical tax 0%, hurdle 4–7% (tax-exempt bond cost + risk premium) — and combine with a sector economics layer of EBITDA margin 3–8%, IT spend 3–5% of revenue, realization factor 0.55–0.65.

**Government / public sector:** use — 13 (tax 0%, hurdle from OMB Circular A-94 or jurisdiction equivalent — typically 3–5% real). Sector economics are program-specific; capture them per-engagement rather than from a generic profile.

**Cooperatives / mutuals (credit unions, member-owned utilities):** use — 13 (tax 0% or reduced, hurdle from member cost of capital — typically 5–8%) and the relevant sector profile above (credit unions → Banking; member-owned utilities → Energy/Utilities) for the economics layer.

**When the profile doesn't fit:** if the client is a clear outlier (e.g., a pure-play crypto firm, a biotech pre-revenue, a holding company with mixed segments), pick the closest profile as starting point and override every field with disclosed values. Document the override and rationale in the Assumptions tab I-rows.

**Profile selection is captured in the engagement config** as `industry_profile: <profile name>`. The skill writes this into the dashboard's Assumptions tab so the audience can see which composite was used.

---

## 3. Existing tech stack baseline

Drives the `tech-pill` solid-vs-dashed treatment in UC modals (`structural-rules.md` — Tech-stack pill treatment).

| Field | Source | Notes |
|---|---|---|
| `existing_stack` | Intake Q + 10-K systems disclosures | List of brand/product strings; matched as keywords against tech-pill text |

**Default keyword set** (industrial mid-cap composite, captured from I14 row):

```
SAP / S/4HANA / Salesforce / CPQ / Einstein / Workday / Adobe /
Experience Cloud / ServiceNow / Snowflake / Azure / Microsoft /
M365 / Office 365 / Power BI / Tableau / Outlook / Teams /
GitHub / Visual Studio / O365 / Dynamics 365 / D365 / Excel
```

**Per engagement:** prune anything the client doesn't use; add anything unique to the client (e.g., a vertical-specific platform). This list is the matcher — anything matched renders solid (`tech-pill`); anything unmatched renders dashed (`tech-pill tech-pill-new`) with the `+` badge.

The Assumptions tab I14 row holds the canonical statement of the existing stack. The `existing_stack` keyword list and the I14 row should agree.

---

## 4. Phase 0 dollar anchor

The Roadmap-tab Phase 0 cards must show an order-of-magnitude shared platform investment, never `TBC`.

| Field | Default for $7B revenue archetype | Scaling guidance |
|---|---|---|
| `phase_0_anchor_label` | `~$8–12M*` | — |
| `phase_0_anchor_explainer` | `Shared platform investment — data + cloud readiness, applied once portfolio-wide` | — |

**Scaling:** roughly **0.10–0.15% of revenue** for industrial mid-cap. Adjust for engagements:

| Revenue tier | Indicative range | Tooltip text |
|---|---|---|
| ~$1B | `~$2–4M` | Same explainer |
| ~$3B | `~$4–8M` | Same explainer |
| ~$7B | `~$8–12M` (default) | Same explainer |
| ~$15B | `~$15–25M` | Same explainer |
| ~$50B+ | `~$50–80M` | Same explainer |

Render as `<strong title="...explainer...">~$X–YM*</strong>` in the Phase 0 One-time cell (see `structural-rules.md` — Phase 0 cards). Asterisk follows the realization-factor convention.

---

## 5. Strategic anchors A1–A8

Every client has different strategic anchors. The set is built from Phase 2 primary-source research.

| Field | Source | Notes |
|---|---|---|
| `anchors` | Phase 2 primary-source research → strategic anchor framework | List of `(code, name, take, why_now)` quadruples |

**Default conventions:**
- Codes are `A1` through `A8` (8 anchors total — see `anchor-specificity.md`)
- Names are short noun phrases (e.g., `Profitable Revenue Growth`, `Margin Expansion`, `Working Capital Optimization`)
- Each anchor's `take` is a 2-sentence claim, citation-linked
- Each anchor's `why_now` is a 1-sentence forcing-function

**Anchor tooltip mechanism** (per `structural-rules.md` — Anchor tooltips): every reference to a code in the body of the dashboard gets a `title=` attribute populated from the engagement's anchor table. Example:

```html
<div class="inflight-anchor" title="A1: Profitable Revenue Growth">Anchor: A1</div>
```

For multi-anchor cards (`Anchor: A2, A3`), the title concatenates: `A2: Margin Expansion · A3: Working Capital Optimization`.

The skill auto-generates these tooltips from `anchors` at render time — do not handwrite them.

---

## 6. Heatmap stops

The AVP Task Analysis heatmap image's gradient stops drive the score-chip bucket boundaries (per `chart-conventions.md` — 6).

| Field | Source | Default |
|---|---|---|
| `heatmap_stops` | Inspect the supplied AVP heatmap image; read the gradient breakpoints | `[0, 40, 46, 52, 58, 65, 71, 77, 83, 90, 100]` |
| `heatmap_colors` | Match the image's actual gradient colors | See `chart-conventions.md` — 6 default palette |

**Override at intake:** if the AVP heatmap image uses different stops, update the bucketing function and CSS classes accordingly. Do not assume the default is correct.

---

## 7. In-flight statuses

The set of in-flight initiative statuses varies by engagement — some clients only have "In production" + "Pilot"; others have a deeper lifecycle.

| Field | Source | Default set |
|---|---|---|
| `inflight_statuses` | Phase 2 research + client-provided backlog | `In production`, `Rolling out`, `Pilot`, `Vendor pilot`, `Vendor evaluation` |

**The in-flight legend** (per `structural-rules.md` — In-flight section) renders one row per status that actually appears in the data. Missing statuses are omitted from the legend.

If the engagement has additional statuses (e.g., `Sunset`, `Deprecated`, `Active collaboration`), add them with a one-line definition each.

---

## 8. Function color palette

Function colors must be unique per engagement and not collide with benefit-class colors.

| Field | Default |
|---|---|
| `cost_savings_color` | `#0C62FB` (Slalom blue) |
| `cost_avoidance_color` | `#0e7a86` (teal-deep) |
| `revenue_uplift_color` | `#FF4D5F` (coral) |

**Function color defaults** (canonical 8-pane palette, validated for distinctness):

| Function pane | Default color |
|---|---|
| `all` | `var(--ink)` |
| `se` (Sales Enablement) | `#1F6FBF` (steel blue) — distinct from Cost savings `#0C62FB` |
| `sc` (Supply Chain) | `#0e7a86` |
| `fin` (Finance) | `#7B61FF` (purple) |
| `it` | `#1BE1F2` (cyan) |
| `mk` (Marketing) | `#FF4D5F` |
| `hr` | `#002FAF` (dark blue) |
| `cs` (Customer Service) | `#F5A623` (amber) |

**Conflict check:** at intake, assert no function color matches `cost_savings_color`, `cost_avoidance_color`, or `revenue_uplift_color`. A prior build had SE = `#0C62FB` colliding with Cost savings = `#0C62FB` — readers couldn't tell whether a blue badge meant "Sales Enablement" or "Cost savings". Fixed by shifting SE to `#1F6FBF`.

When the engagement has fewer than 7 functions, drop the extra colors rather than reusing the same color for two purposes.

---

## 9. In-scope functions and acronym list

Different engagements have different functional acronyms. The first-use spell-out list (per `editorial-rules.md` — First-use spell-outs) varies by which functions are in scope.

| Function | Function-specific acronyms to spell out |
|---|---|
| Sales Enablement | CPQ, ATS, ICP |
| Supply Chain | OEE, IBP, S&OP, MAPE |
| Finance | FP&A, AP/AR, DSO, DPO, DOH, CCC |
| IT | SOC, ITSM, M365, SRE |
| Marketing, eCommerce & Digital | MMM, CDP, DTC, NPS, AOV, GMV |
| HR & People | TA, HRIS, NPS-eX |
| Customer Service | AHT, IVR, FCR, CSAT, deflection |

**Universal acronyms** (always spell out on first use, regardless of function): P50, NPV, IRR, WACC, hurdle rate, UC, AVP, L3 task, LOE, WBS, Big Four (Deloitte, EY, KPMG, PwC).

**The glossary panel** (Summary tab, `<details open>`) renders both: the universal financial+AVP terms (always) plus any function-specific acronyms triggered by the in-scope functions.

---

## 10. "Used for" source mapping

The Sources tab Primary sources table carries a `Used for` column mapping each citation to where it lands in the dashboard.

| Field | Source | Notes |
|---|---|---|
| `source_used_for` | Auto-extracted from `routeCite` and `href="#ref-..."` calls in the rendered HTML | Map of source ID → list of "tab · section" strings |

The skill walks the rendered HTML at delivery, finds every citation reference, and back-fills the `Used for` column per source ID. Manual editing is allowed but the auto-extraction is the source of truth — re-render after any citation change.

For research/benchmark sources that ground a strategic anchor (10-Ks for A1–A8), the `Used for` column reads `A{n}: {anchor name} · {tab}` so the reader can trace the citation chain.

---

## 11. Output size budget

Per `qa-checklist.md` — File size sanity, the rendered HTML has size discipline:

| Image count (heatmap PNGs in AVP Analysis tab) | Target HTML size | Hard cap |
|---|---|---|
| 0 | < 5 MB | 8 MB |
| 1 | 5–8 MB | 12 MB |
| 2–3 | 8–18 MB | 22 MB |
| 4+ | 18–35 MB | 50 MB |

If the file exceeds the hard cap, externalise the heaviest assets (XLSX downloads, heatmap PNGs) and link to them via filesystem paths or signed URLs. A prior 17 MB build with all assets embedded caused a 652 MB transcript blow-up in a long editing session — the file format is fine for delivery, but for iteration/editing prefer external references.

---

## 12. Engagement config template

Use this template at intake. Save as `engagement-config-{client}.md` alongside the AVP exports.

```markdown
# Engagement: <Client name>

## Revenue and archetype
- revenue_usd: $X.XB
- revenue_label: "$XB <industry> <archetype descriptor>"

## Industry composite
- industry_profile: <one of: financial-services-banking | financial-services-insurance | saas-tech | retail | hospitality | telco | industrial-manufacturing | energy-utilities | custom>  # REQUIRED — see — 2a
- wacc_pct: X.X
- hurdle_rate_pct: X.X
- ebitda_margin_pct: X.X       # or sector proxy per — 2a (e.g., efficiency ratio for banking)
- effective_tax_rate_pct: XX
- working_capital_usd: $X.XB   # or sector proxy where WC framing doesn't apply
- it_spend_ratio_pct: X.X
- marketing_spend_ratio_pct: X.X
- headcount: NN,NNN
- monte_carlo_horizon_yrs: 5
- portfolio_realization_factor: 0.XX  # from — 2a profile; tighten with client-validated parameters

## Phase 0 anchor
- phase_0_anchor_label: ~$X–YM*
- phase_0_anchor_explainer: <text>

## Existing tech stack
- existing_stack: [brand1, brand2, ...]

## Strategic anchors
- A1 / <name> / <take> / <why now>
- A2 / ... / ... / ...
- ...

## Heatmap stops
- heatmap_stops: [0, 40, 46, 52, 58, 65, 71, 77, 83, 90, 100]
- heatmap_colors: <list of 10 hex>  (default: see chart-conventions.md — 6)

## In-flight statuses
- inflight_statuses: [In production, Rolling out, Pilot, Vendor pilot, Vendor evaluation]

## Function color palette
- all / <fn-color>
- se / <fn-color>
- ...

## In-scope functions
- functions: [se, sc, fin, it, mk, hr, cs]
- function_specific_acronyms: <list>

## Cost mode (v2.2)
- cost_mode: optimized   # standard | optimized | full-fidelity — default optimized
- opt_in_levers: []      # any of: multi-session, externalized-assets, haiku-qa

## Financial structure
- structure_type: [for-profit / tax-exempt-nonprofit / government / cooperative / sovereign]
- effective_tax_rate_pct: XX
- hurdle_rate_pct: X.X
- hurdle_basis: "<explain: e.g., 'AA+/Aa1 bond rating; tax-exempt cost of debt ~3.5% + 2% risk premium'>"
- npv_caveat_required: [yes / no]  (auto-set yes if tax < 10% AND hurdle < 8%)

## Benefit class overrides (leave blank to use defaults)
- override_incremental_revenue: "<new label or blank>"
- override_hard_cost_reduction: "<new label or blank>"
- override_revenue_assurance: "<new label or blank>"
- override_productivity_savings: "<new label or blank>"
- override_cost_avoidance: "<new label or blank>"

## Non-financial value
- nfv_weight: 0.00  (0.00 = off; 0.10-0.25 = active)
- nfv_category: "<e.g., 'Mission & patient outcomes'>"
- nfv_badge_label: "<e.g., 'Mission & outcomes'>"   # text only — emoji badges are a QA hard-fail (client-language.md)
- nfv_badge_emoji: ""   # leave blank — emoji in visible badges is forbidden

## Design variant
- design_variant: canonical   # canonical | multifile | extended | <custom name>
- design_overlay_path: ""     # path to references/design-variants/<name>.md when non-canonical; empty for canonical
```

The intake checklist (`intake-checklist.md`) walks the user through populating this. Do not start Phase 3 (bundling) until every section is filled or has documented defaults.

---

## 13. Financial structure override

Not every organization uses the default 10.5% hurdle / 30% tax composite. Capture the actual financial structure at intake and override defaults accordingly.

| Structure | Tax rate | Hurdle guidance | P(NPV>0) caveat required? |
|---|---|---|---|
| **For-profit corporation** (default) | 22–30% | WACC + 3–5% risk premium (default 10.5%) | No |
| **Tax-exempt nonprofit** (e.g., 501(c)(3) health systems, foundations) | 0% | Tax-exempt bond cost of debt + 1–2% (typically 4–7%) | Yes |
| **Government / public sector** | 0% | OMB Circular A-94 rate or equivalent jurisdiction discount rate | Yes |
| **Cooperative / mutual** (e.g., credit unions, member-owned utilities) | 0% or reduced | Member cost of capital or regulatory return-on-equity | Yes |
| **Sovereign-backed / state-owned** | Varies by jurisdiction | Sovereign cost of funds + 1–2% | Depends on tax position |

**When the caveat is required:** Add this note to the Assumptions tab model methodology section and to the Summary tab hero caveat:

> *"This organization's financial structure (X% tax rate, Y% hurdle) produces structurally high NPV and P(NPV>0) relative to for-profit benchmarks. This reflects the organization's actual cost of capital, not optimistic estimation. Payback months and the per-use-case formula basis — not NPV probability — are the appropriate credibility anchors for this portfolio."*

**Decision rule:** If `effective_tax_rate_pct` < 10% AND `hurdle_rate_pct` < 8%, the caveat is mandatory. The combination eliminates most of the discount and tax drag that normally constrain NPV, meaning even modestly-sized benefits produce positive NPV in nearly all MC scenarios.

---

## 16. Design variant

The skill ships a canonical Slalom design system (the default) and two named overlay variants for engagements where the user has historically requested a different visual lineage.

| Variant | When | Overlay file |
|---|---|---|
| **canonical** (default) | Every engagement unless otherwise specified | None — `design.md` is the source of truth |
| **multifile** | Explicit request for the Multifile styling lineage (external CSS + Google Fonts) | `references/design-variants/multifile.md` |
| **extended** | Explicit request for the Extended styling lineage (extended palette + extra tabs) | `references/design-variants/extended.md` |
| **custom** | New variant requested at intake | New file in `references/design-variants/<name>.md`, written during intake |

**Selection happens at intake** — see `intake-checklist.md` — Question 22.

**Default is canonical** — non-canonical variants apply only when the user explicitly selects one. Canonical builds compare against the golden master per `references/golden-master.md`.

**Captured fields:**

```
design_variant: canonical | multifile | extended | <custom name>
design_overlay_path: <empty for canonical; path to overlay file for variants>
```

**Non-canonical builds:** the overlay file declares what it overrides; the canonical rules in `design.md` apply where the overlay is silent. QA still runs — adapt CSS-specific checks to the overlay's file structure when needed.

---

## 14. Benefit class overrides

The default 5-class benefit taxonomy (Hard cost reduction / Productivity savings / Cost avoidance / Revenue assurance / Incremental revenue) and 3-bucket executive roll-up work for most for-profit engagements. For non-standard organizations or audiences, any class name can be overridden per engagement.

**The override changes the label, not the calculation.** The underlying financial math is identical — only the client-facing name changes. The override applies everywhere the class appears: hero, KPI strip, per-UC modal pill, phasing cards, Assumptions tab definitions.

| Default class | When to override | Example overrides |
|---|---|---|
| **Incremental revenue** | Organization doesn't frame growth as "revenue" or "top line" | "Access & capacity utilization" (health system), "Constituent service capacity" (government), "Member value growth" (cooperative), "Mission delivery expansion" (nonprofit) |
| **Hard cost reduction** | Audience is sensitive to "cost cutting" language | "Operational efficiency" (any), "Resource optimization" (public sector), "Stewardship savings" (nonprofit) |
| **Revenue assurance** | Organization doesn't use "revenue" framing | "Reimbursement integrity" (health system), "Fund recovery" (government), "Rate-base protection" (regulated utility) |

**The 3-bucket executive roll-up also overrides accordingly.** If "Incremental revenue" becomes "Access & capacity utilization," the third bucket label changes too.

---

## 15. Non-financial value weight

Some use cases exist primarily for non-financial reasons — patient safety, regulatory compliance, environmental impact, equity, or mission delivery. These may be break-even or net-negative financially but still belong in the portfolio because the audience values the outcome independently of ROI.

**The non-financial value flag is a boolean on each UC.** UCs flagged `true` receive additional weight in the composite ranking (see `monte-carlo.md` — Composite ranking) to prevent them from being auto-cut during downselection.

| Sector | Non-financial value examples | Default composite weight |
|---|---|---|
| **Commercial / for-profit** (default) | — | 0.00 (financial-only ranking) |
| **Healthcare / nonprofit** | Patient outcomes, health equity, clinician wellbeing, community benefit | 0.20–0.25 |
| **Government / public sector** | Constituent access, equity, public safety, service delivery | 0.20–0.25 |
| **Regulated industry** (energy, financial services) | Safety-critical systems, compliance-mandatory, grid reliability | 0.15–0.20 |
| **ESG-committed** (any sector) | Environmental impact, DEI outcomes, community investment | 0.10–0.15 |

**Default:** 0.00 (commercial for-profit). Set higher only when the user confirms the audience values non-financial outcomes in portfolio selection.

**Display:** Flagged UCs carry a visible badge in the portfolio table and modals. The badge label is configurable: "Mission & outcomes" (healthcare), "Safety-critical" (energy/manufacturing), "Compliance-mandatory" (financial services), "ESG impact" (any). Text labels only — emoji badges are a QA hard-fail (see `client-language.md`). Capture the label in the engagement config.
